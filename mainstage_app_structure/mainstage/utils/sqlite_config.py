import sqlite3
import os

# ✅ Set database file path relative to this file
DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'mainstage.db')

# ✅ Function to connect to the SQLite database
def connect():
    return sqlite3.connect(DB_FILE)

# ✅ Function to create the 'posts' table if it doesn't exist
def create_posts_table():
    conn = connect()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            username TEXT,
            content TEXT,
            image_url TEXT,
            timestamp TEXT
        );
    ''')
    conn.commit()
    conn.close()
