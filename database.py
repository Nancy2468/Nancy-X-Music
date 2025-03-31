import sqlite3

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
