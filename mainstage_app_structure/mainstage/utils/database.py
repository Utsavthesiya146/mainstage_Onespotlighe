import sqlite3
import os
from datetime import datetime

# ✅ Set database file path
DB_FILE = os.path.join(os.path.dirname(__file__), '..', 'mainstage.db')

# ✅ Initialize the database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # 🧑 Create users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            bio TEXT,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 🗳️ Create votes table
    c.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            voter_name TEXT,
            voted_user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # 🌟 Create spotlight table
    c.execute("""
        CREATE TABLE IF NOT EXISTS spotlight (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            started_at TIMESTAMP
        );
    """)

    # 📸 Create posts table (if needed)
    c.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            username TEXT,
            content TEXT,
            image_url TEXT,
            timestamp TEXT
        );
    """)

    conn.commit()
    conn.close()

# ✅ Create new user
def create_user(name, bio, image_url):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO users (name, bio, image_url) VALUES (?, ?, ?)", (name, bio, image_url))
    conn.commit()
    conn.close()

# ✅ Get user by name (for login)
def get_user_by_name(name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name, bio, image_url FROM users WHERE name = ?", (name,))
    user = c.fetchone()
    conn.close()
    return user

# ✅ Update existing user (for Profile Edit feature)
def update_user(user_id, name, bio, image_url=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    if image_url:
        c.execute("""
            UPDATE users
            SET name = ?, bio = ?, image_url = ?
            WHERE id = ?
        """, (name, bio, image_url, user_id))
    else:
        c.execute("""
            UPDATE users
            SET name = ?, bio = ?
            WHERE id = ?
        """, (name, bio, user_id))

    conn.commit()
    conn.close()

# ✅ Get all users
def get_all_users():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name, bio, image_url FROM users")
    users = c.fetchall()
    conn.close()
    return users

# ✅ Save vote
def save_vote(voter_name, voted_user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO votes (voter_name, voted_user_id) VALUES (?, ?)", (voter_name, voted_user_id))
    conn.commit()
    conn.close()

# ✅ Get top voted user
def get_top_voted_user():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT voted_user_id, COUNT(*) as vote_count
        FROM votes
        GROUP BY voted_user_id
        ORDER BY vote_count DESC
        LIMIT 1;
    """)
    top = c.fetchone()
    conn.close()
    return top

# ✅ Save new spotlight
def save_spotlight_user(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute("INSERT INTO spotlight (user_id, started_at) VALUES (?, ?)", (user_id, now))
    conn.commit()
    conn.close()

# ✅ Get current spotlight user
def get_spotlight_user():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user_id, started_at FROM spotlight ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    return row if row else (None, None)

# ✅ Get leaderboard users
def get_leaderboard():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT users.name, users.image_url, COUNT(votes.id) as vote_count
        FROM users
        LEFT JOIN votes ON users.id = votes.voted_user_id
        GROUP BY users.id
        ORDER BY vote_count DESC
        LIMIT 10;
    """)
    leaders = c.fetchall()
    conn.close()
    return leaders

# ✅ Save post
def save_post(user_id, username, content, image_url=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("""
        INSERT INTO posts (user_id, username, content, image_url, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, username, content, image_url, now))
    conn.commit()
    conn.close()

# ✅ Get all posts (latest first)
def get_all_posts():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        SELECT username, content, image_url, timestamp
        FROM posts
        ORDER BY id DESC
    """)
    rows = c.fetchall()
    conn.close()

    posts = []
    for row in rows:
        posts.append({
            "username": row[0],
            "content": row[1],
            "image_url": row[2],
            "timestamp": row[3]
        })
    return posts
