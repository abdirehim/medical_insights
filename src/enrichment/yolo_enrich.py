import os
import logging
from datetime import datetime
from ultralytics import YOLO
import psycopg2
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
IMAGES_DIR = os.path.join("data", "raw", "images")
MODEL_PATH = "yolov8n.pt"  # Use YOLOv8 nano model for speed; replace with custom if needed

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/enrichment.log"),
        logging.StreamHandler()
    ]
)

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except psycopg2.OperationalError as e:
        logging.error(f"Database connection failed: {e}")
        return None

def enrich_images():
    model = YOLO(MODEL_PATH)
    logging.info(f"Loaded YOLOv8 model from {MODEL_PATH}")

    for channel in os.listdir(IMAGES_DIR):
        channel_dir = os.path.join(IMAGES_DIR, channel)
        if not os.path.isdir(channel_dir):
            continue
        for img_file in os.listdir(channel_dir):
            if not img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                continue
            img_path = os.path.join(channel_dir, img_file)
            try:
                results = model(img_path)
                for result in results:
                    for box in result.boxes:
                        # Prepare enrichment data
                        object_class = model.names[int(box.cls)]
                        confidence = float(box.conf)
                        bbox = box.xyxy[0].tolist()  # [xmin, ymin, xmax, ymax]
                        logging.info(f"Detected {object_class} (conf: {confidence:.2f}) in {img_file}")
                        # TODO: Insert enrichment result into DB
                        # insert_enrichment_to_db(...)
            except Exception as e:
                logging.error(f"Error processing {img_path}: {e}")

def main():
    logging.info("Starting YOLOv8 image enrichment...")
    enrich_images()
    logging.info("Enrichment complete.")

if __name__ == "__main__":
    main() 