import sqlite3
from config import load_config
from sqlalchemy import create_engine

# Load the configuration data
config_data = load_config()

def add_music_group(chat_id):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO music_groups (chat_id) VALUES (?)", (chat_id,))
    conn.commit()
    conn.close()

def remove_music_group(chat_id):
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM music_groups WHERE chat_id = ?", (chat_id,))
    conn.commit()
    conn.close()

def get_music_groups():
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT chat_id FROM music_groups")
    groups = [str(row[0]) for row in cursor.fetchall()]
    conn.close()
    return groups
def add_admin(user_id):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO admins (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def is_admin_db(user_id):
    conn = sqlite3.connect("bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM admins WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Access the database_url
database_url = config_data.get('database_url')

# Use the database_url to create a connection to the database
def connect_to_database():
    engine = create_engine(database_url)
    with engine.connect() as connection:
        # Perform database operations
        result = connection.execute("SELECT * FROM your_table")
        for row in result:
            print(row)
            



class Database:
    def __init__(self, db_name="music_bot.db"):
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            name TEXT
        )
        ""
        )
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            playlist_name TEXT,
            song TEXT
        )
        ""
        )
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            user_id INTEGER
        )
        ""
        )
        
        self.connection.commit()
    
    def add_playlist(self, chat_id, name):
        self.cursor.execute("INSERT INTO playlists (chat_id, name) VALUES (?, ?)", (chat_id, name))
        self.connection.commit()
    
    def remove_playlist(self, chat_id, name):
        self.cursor.execute("DELETE FROM playlists WHERE chat_id = ? AND name = ?", (chat_id, name))
        self.cursor.execute("DELETE FROM songs WHERE chat_id = ? AND playlist_name = ?", (chat_id, name))
        self.connection.commit()
    
    def get_all_playlists(self, chat_id):
        self.cursor.execute("SELECT name FROM playlists WHERE chat_id = ?", (chat_id,))
        return [row[0] for row in self.cursor.fetchall()]
    
    def add_song(self, chat_id, playlist_name, song):
        self.cursor.execute("INSERT INTO songs (chat_id, playlist_name, song) VALUES (?, ?, ?)", (chat_id, playlist_name, song))
        self.connection.commit()
    
    def remove_song(self, chat_id, playlist_name, song):
        self.cursor.execute("DELETE FROM songs WHERE chat_id = ? AND playlist_name = ? AND song = ?", (chat_id, playlist_name, song))
        self.connection.commit()
    
    def get_playlist(self, chat_id, playlist_name):
        self.cursor.execute("SELECT song FROM songs WHERE chat_id = ? AND playlist_name = ?", (chat_id, playlist_name))
        return [row[0] for row in self.cursor.fetchall()]
    
    def add_admin(self, chat_id, user_id):
        self.cursor.execute("INSERT INTO admins (chat_id, user_id) VALUES (?, ?)", (chat_id, user_id))
        self.connection.commit()
    
    def remove_admin(self, chat_id, user_id):
        self.cursor.execute("DELETE FROM admins WHERE chat_id = ? AND user_id = ?", (chat_id, user_id))
        self.connection.commit()
    
    def get_admins(self, chat_id):
        self.cursor.execute("SELECT user_id FROM admins WHERE chat_id = ?", (chat_id,))
        return [row[0] for row in self.cursor.fetchall()]
    
    def is_admin(self, chat_id, user_id):
        self.cursor.execute("SELECT 1 FROM admins WHERE chat_id = ? AND user_id = ?", (chat_id, user_id))
        return self.cursor.fetchone() is not None

    def add_song_to_drive(group_id, playlist_name, song_path, song_name):
    # Upload to Google Drive
    file_drive = drive.CreateFile({"title": song_name})
    file_drive.SetContentFile(song_path)
    file_drive.Upload()
    file_url = f"https://drive.google.com/file/d/{file_drive['id']}/view"

    # Store in database
    cursor.execute("INSERT INTO songs (playlist_id, song_name, song_url) VALUES ((SELECT id FROM playlists WHERE group_id = ? AND name = ?), ?, ?)",
                   (group_id, playlist_name, song_name, file_url))
    conn.commit()
    return file_url
