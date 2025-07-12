"""
telegram_scraper.py

Scrapes messages and images from public Ethiopian medical Telegram channels, saves raw data as JSON, and loads it into PostgreSQL for downstream analytics. Implements robust error handling, deduplication, and logging for production-ready data engineering pipelines.
"""

import os
import json
import logging
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import psycopg2
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import FloodWaitError, ChannelPrivateError

# --- Configuration ---
load_dotenv()

API_ID = os.getenv("TELEGRAM_API_ID")  # Telegram API ID from .env
API_HASH = os.getenv("TELEGRAM_API_HASH")  # Telegram API Hash from .env
PHONE = os.getenv("TELEGRAM_PHONE")  # Telegram phone number
PASSWORD = os.getenv("TELEGRAM_PASSWORD")  # Telegram password (if 2FA enabled)
TELEGRAM_CODE = os.getenv("TELEGRAM_CODE")  # Telegram login code (if needed)
DATABASE_URL = os.getenv("DATABASE_URL")  # PostgreSQL connection string

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/scrape.log"),
        logging.StreamHandler()
    ]
)

# --- Channel Lists ---
# List of Telegram channels to scrape for text and images
TEXT_CHANNELS = [
    "Thequorachannel",
    "lobelia4cosmetics",
    "tikvahpharma",
    "tenamereja",
    "CheMed123"
]

IMAGE_CHANNELS = [
    "lobelia4cosmetics",
    "CheMed123"
]

# --- Database Functions ---
def get_db_connection():
    """Establishes a connection to the PostgreSQL database using DATABASE_URL."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.OperationalError as e:
        logging.error(f"Database connection failed: {e}")
        return None

def setup_database():
    """Creates the raw.telegram_messages table if it does not exist."""
    conn = get_db_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE SCHEMA IF NOT EXISTS raw;
            CREATE TABLE IF NOT EXISTS raw.telegram_messages (
                id SERIAL PRIMARY KEY,
                channel_name VARCHAR(255),
                message_id INT,
                data JSONB,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(channel_name, message_id)
            );
            """)
        conn.commit()
        conn.close()
        logging.info("Database schema and table verified.")

def insert_message_to_db(channel_name, message_id, message_data):
    """Inserts a single message into the raw.telegram_messages table. Uses ON CONFLICT to avoid duplicates."""
    conn = None
    try:
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO raw.telegram_messages (channel_name, message_id, data)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (channel_name, message_id) DO NOTHING;
                    """,
                    (channel_name, message_id, json.dumps(message_data, default=str))
                )
            conn.commit()
            logging.info(f"Inserted message {message_id} from {channel_name} into DB.")
    except psycopg2.Error as e:
        logging.error(f"Database insertion failed for message {message_id} from {channel_name}: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

# --- Data Lake Functions ---
def save_to_json(channel_name, message_data):
    """Saves message data to a local JSON file in data/raw/telegram_messages/YYYY-MM-DD/channel_name.json."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    dir_path = os.path.join("data", "raw", "telegram_messages", date_str)
    os.makedirs(dir_path, exist_ok=True)
    
    file_path = os.path.join(dir_path, f"{channel_name}.json")
    with open(file_path, 'a', encoding='utf-8') as f:
        json.dump(message_data, f, ensure_ascii=False, default=str)
        f.write('\n')

# --- Scraper ---
async def scrape_channel(client, channel_name):
    """Scrapes a single Telegram channel for messages and images. Downloads images for IMAGE_CHANNELS."""
    logging.info(f"Scraping channel: {channel_name}")
    try:
        entity = await client.get_entity(channel_name)
        messages = await client.get_messages(entity, limit=100)  # Limit for demonstration

        for message in messages:
            if message.text or message.photo:
                message_dict = message.to_dict()
                
                # Save to Data Lake (JSON)
                save_to_json(channel_name, message_dict)

                # Insert to PostgreSQL
                insert_message_to_db(channel_name, message.id, message_dict)

                # Download images if channel is in the image list
                if channel_name in IMAGE_CHANNELS and message.photo:
                    image_dir = os.path.join("data", "raw", "images", channel_name)
                    os.makedirs(image_dir, exist_ok=True)
                    await client.download_media(
                        message.photo,
                        file=os.path.join(image_dir, f"{message.id}.jpg")
                    )
                    logging.info(f"Downloaded image {message.id} from {channel_name}")

    except FloodWaitError as e:
        logging.warning(f"Rate limit hit for {channel_name}. Waiting {e.seconds} seconds.")
        await asyncio.sleep(e.seconds)
    except ChannelPrivateError:
        logging.warning(f"Cannot access private channel: {channel_name}. Skipping.")
    except Exception as e:
        logging.error(f"Could not process channel {channel_name}: {e}")

# --- Main Execution ---
async def main():
    """Main function to orchestrate the scraping process: sets up DB, authenticates, and scrapes all channels."""
    if not all([API_ID, API_HASH, DATABASE_URL]):
        logging.error("Missing required environment variables. Exiting.")
        return

    setup_database()

    # The session file will be created in the root of the project
    client = TelegramClient('anon', API_ID, API_HASH)
    await client.start(phone=PHONE, password=PASSWORD)
    logging.info("Client created and authenticated. Scraping will begin shortly.")
    
    all_channels = set(TEXT_CHANNELS + IMAGE_CHANNELS)
    for channel in all_channels:
        await scrape_channel(client, channel)
        
    logging.info("Scraping finished.")
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())

# End of script

