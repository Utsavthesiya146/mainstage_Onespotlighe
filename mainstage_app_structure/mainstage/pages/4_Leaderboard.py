import streamlit as st
import sqlite3
import os
from utils.database import DB_FILE

def get_leaderboard():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT users.name, users.image_url, COUNT(votes.id) as vote_count
        FROM users
        LEFT JOIN votes ON users.id = votes.voted_user_id
        GROUP BY users.id
        ORDER BY vote_count DESC
        LIMIT 10;
    """)
    results = cursor.fetchall()
    conn.close()
    return results

# Set page config
st.set_page_config(page_title="🏆 Leaderboard", layout="centered")
st.title("🏆 MainStage Leaderboard")

# Load leaders
leaders = get_leaderboard()

if leaders:
    for i, (name, image_url, votes) in enumerate(leaders, start=1):
        col1, col2 = st.columns([1, 6])

        with col1:
            # ✅ Show user's image if available and file exists
            if image_url and os.path.exists(image_url):
                st.image(image_url, width=60)
            else:
                # 🖼️ Show app logo if user has no image
                st.image("D:\\mainstage_app_structure\\mainstage\\assets\\logo.png", width=60)

        with col2:
            st.markdown(f"### {i}. {name}")
            st.markdown(f"⭐ **Votes:** `{votes}`")
            st.markdown("---")
else:
    st.info("No votes yet. Be the first to shine! ✨")
