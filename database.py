import sqlite3

class Database:
    def __init__(self, db_path="database.sqlite"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.setup()

    def setup(self):
        # Create tables for users, playlists, songs, and queues
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                group_id INTEGER PRIMARY KEY,
                owner_id INTEGER,
                admin_ids TEXT
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlists (
                group_id INTEGER,
                playlist_name TEXT,
                song_urls TEXT,
                PRIMARY KEY (group_id, playlist_name)
            )
        """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS queue (
                group_id INTEGER,
                song_url TEXT,
                added_by INTEGER
            )
        """)
        
        self.conn.commit()

    def add_group(self, group_id, owner_id, admin_ids):
        admin_ids_str = ",".join(map(str, admin_ids))
        self.cursor.execute("""
            INSERT OR REPLACE INTO groups (group_id, owner_id, admin_ids) VALUES (?, ?, ?)
        """, (group_id, owner_id, admin_ids_str))
        self.conn.commit()
    
    def get_admins(self, group_id):
        self.cursor.execute("SELECT admin_ids FROM groups WHERE group_id = ?", (group_id,))
        result = self.cursor.fetchone()
        return list(map(int, result[0].split(","))) if result else []
    
    def add_playlist(self, group_id, playlist_name, song_urls):
        song_urls_str = ",".join(song_urls)
        self.cursor.execute("""
            INSERT OR REPLACE INTO playlists (group_id, playlist_name, song_urls) VALUES (?, ?, ?)
        """, (group_id, playlist_name, song_urls_str))
        self.conn.commit()
    
    def get_playlist(self, group_id, playlist_name):
        self.cursor.execute("""
            SELECT song_urls FROM playlists WHERE group_id = ? AND playlist_name = ?
        """, (group_id, playlist_name))
        result = self.cursor.fetchone()
        return result[0].split(",") if result else []
    
    def remove_playlist(self, group_id, playlist_name):
        self.cursor.execute("DELETE FROM playlists WHERE group_id = ? AND playlist_name = ?", (group_id, playlist_name))
        self.conn.commit()
    
    def add_to_queue(self, group_id, song_url, added_by):
        self.cursor.execute("""
            INSERT INTO queue (group_id, song_url, added_by) VALUES (?, ?, ?)
        """, (group_id, song_url, added_by))
        self.conn.commit()
    
    def get_queue(self, group_id):
        self.cursor.execute("SELECT song_url FROM queue WHERE group_id = ?", (group_id,))
        return [row[0] for row in self.cursor.fetchall()]
    
    def clear_queue(self, group_id):
        self.cursor.execute("DELETE FROM queue WHERE group_id = ?", (group_id,))
        self.conn.commit()
    
    def close(self):
        self.conn.close()

# Usage Example:
# db = Database()
# db.add_group(group_id=123456, owner_id=789012, admin_ids=[111, 222, 333])
# print(db.get_admins(123456))
# db.add_playlist(123456, "My Playlist", ["song1.mp3", "song2.mp3"])
# print(db.get_playlist(123456, "My Playlist"))
