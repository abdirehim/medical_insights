
import unittest
import os
import json
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

from telethon.errors.rpcerrorlist import FloodWaitError, ChannelPrivateError

# Import the functions to be tested
from src.scrape.telegram_scraper import save_to_json, scrape_channel, get_db_connection, setup_database, insert_message_to_db

class TestScraper(unittest.TestCase):

    @patch('src.scrape.telegram_scraper.os.makedirs')
    @patch('builtins.open')
    def test_save_to_json(self, mock_open, mock_makedirs):
        """Test that message data is correctly written to a JSON file."""
        channel_name = "test_channel"
        message_data = {"id": 123, "text": "hello world"}
        
        date_str = "2025-07-12"
        dir_path = os.path.join("data", "raw", "telegram_messages", date_str)
        file_path = os.path.join(dir_path, f"{channel_name}.json")

        with patch('src.scrape.telegram_scraper.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = date_str
            save_to_json(channel_name, message_data)
            mock_makedirs.assert_called_with(dir_path, exist_ok=True)
            mock_open.assert_called_with(file_path, 'a', encoding='utf-8')
            mock_file = mock_open.return_value.__enter__.return_value
            mock_file.write.assert_any_call(json.dumps(message_data, ensure_ascii=False, default=str))

    @patch('src.scrape.telegram_scraper.psycopg2.connect')
    def test_get_db_connection_success(self, mock_connect):
        """Test successful database connection."""
        mock_connect.return_value = MagicMock()
        self.assertIsNotNone(get_db_connection())

    @patch('src.scrape.telegram_scraper.psycopg2.connect')
    def test_get_db_connection_failure(self, mock_connect):
        """Test database connection failure."""
        mock_connect.side_effect = Exception("Connection failed")
        self.assertIsNone(get_db_connection())

    @patch('src.scrape.telegram_scraper.get_db_connection')
    def test_setup_database(self, mock_get_conn):
        """Test that the database setup function executes commands."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        
        setup_database()
        
        self.assertTrue(mock_cursor.execute.called)
        self.assertTrue(mock_conn.commit.called)
        self.assertTrue(mock_conn.close.called)

    @patch('src.scrape.telegram_scraper.get_db_connection')
    def test_insert_message_to_db_success(self, mock_get_conn):
        """Test successful message insertion into the database."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        from src.scrape.telegram_scraper import insert_message_to_db
        insert_message_to_db("test_channel", 1, {"text": "test"})

        self.assertTrue(mock_cursor.execute.called)
        self.assertTrue(mock_conn.commit.called)
        self.assertTrue(mock_conn.close.called)

    @patch('src.scrape.telegram_scraper.get_db_connection')
    @patch('src.scrape.telegram_scraper.logging')
    def test_insert_message_to_db_failure(self, mock_logging, mock_get_conn):
        """Test database insertion failure handling."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = Exception("DB Error")

        from src.scrape.telegram_scraper import insert_message_to_db
        insert_message_to_db("test_channel", 1, {"text": "test"})

        self.assertTrue(mock_logging.error.called)
        self.assertTrue(mock_conn.rollback.called)
        self.assertTrue(mock_conn.close.called)

class TestAsyncScraper(unittest.IsolatedAsyncioTestCase):

    @patch('src.scrape.telegram_scraper.save_to_json')
    @patch('src.scrape.telegram_scraper.insert_message_to_db')
    @patch('src.scrape.telegram_scraper.os.makedirs')
    async def test_scrape_channel_success(self, mock_makedirs, mock_insert_message_to_db, mock_save_to_json):
        """Test successful scraping of a channel, including image download and DB insertion."""
        mock_client = AsyncMock()
        mock_message = MagicMock()
        mock_message.text = "Test message"
        mock_message.photo = True
        mock_message.id = 456
        mock_message.to_dict.return_value = {"id": 456, "text": "Test message"}
        
        mock_client.get_messages.return_value = [mock_message]
        
        channel_name = "CheMed123" # A channel that should have images
        await scrape_channel(mock_client, channel_name)

        mock_client.get_entity.assert_called_with(channel_name)
        mock_save_to_json.assert_called_with(channel_name, {"id": 456, "text": "Test message"})
        mock_insert_message_to_db.assert_called_with(channel_name, 456, {"id": 456, "text": "Test message"})
        mock_client.download_media.assert_called()

    @patch('src.scrape.telegram_scraper.logging')
    async def test_scrape_channel_flood_wait_error(self, mock_logging):
        """Test that FloodWaitError is handled correctly."""
        mock_client = AsyncMock()
        mock_client.get_entity.side_effect = FloodWaitError(seconds=5)
        
        with patch('asyncio.sleep', new_callable=AsyncMock) as mock_sleep:
            await scrape_channel(mock_client, "some_channel")
            mock_sleep.assert_called_with(5)
            self.assertTrue(mock_logging.warning.called)

    @patch('src.scrape.telegram_scraper.logging')
    async def test_scrape_channel_private_error(self, mock_logging):
        """Test that ChannelPrivateError is handled correctly."""
        mock_client = AsyncMock()
        mock_client.get_entity.side_effect = ChannelPrivateError("The channel is private")
        
        await scrape_channel(mock_client, "private_channel")
        self.assertTrue(mock_logging.warning.called)
        mock_logging.warning.assert_called_with("Cannot access private channel: private_channel. Skipping.")

if __name__ == '__main__':
    unittest.main()
