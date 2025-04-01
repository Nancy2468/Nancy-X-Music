import os
from dotenv import load_dotenv
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import json

load_dotenv()

# Telegram API Configuration
API_ID = int(os.getenv("API_ID", ""))  # Get from my.telegram.org
API_HASH = os.getenv("API_HASH", "")  # Get from my.telegram.org
BOT_TOKEN = os.getenv("BOT_TOKEN", "")  # Get from BotFather

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "database.sqlite")

# Google Drive Configuration
GDRIVE_FOLDER_ID = os.getenv("GDRIVE_FOLDER_ID", "")  # Folder ID for storing playlists and songs
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# Bot Settings
OWNER_ID = int(os.getenv("OWNER_ID", ""))  # Your Telegram user ID
ADMINS = list(map(int, os.getenv("ADMINS", "").split()))  # List of admin IDs

# Music Playback Configuration
VOICE_CHAT_TIMEOUT = 360  # Auto-stop if no one in voice chat for 6 minutes
INLINE_BUTTON_LIFETIME = 300  # Inline buttons disappear after 5 minutes

# Scheduled Messages
GOOD_MORNING_TIME = "07:00"  # 7 AM
GOOD_NIGHT_TIME = "22:00"  # 10 PM

# Function to load the configuration data from the config.json file
def load_config():
    json_file_path = 'config.json'  # Path to your JSON file
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            config_data = json.load(f)
        return config_data
    else:
        raise FileNotFoundError(f"The file {json_file_path} does not exist.")
