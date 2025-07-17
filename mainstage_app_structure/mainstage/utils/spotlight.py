from datetime import datetime, timedelta
from utils.database import (
    get_spotlight_user,
    get_top_voted_user,
    save_spotlight_user
)

# 🔁 Rotate spotlight every 24 hours
def rotate_spotlight():
    current_user_id, started_at = get_spotlight_user()

    if not started_at:
        # No spotlight yet — pick top user now
        top_user = get_top_voted_user()
        if top_user:
            save_spotlight_user(top_user[0])
        return

    started_time = datetime.fromisoformat(started_at)
    now = datetime.now()

    # ⏳ Check if 24 hours passed
    if now - started_time >= timedelta(hours=24):
        top_user = get_top_voted_user()
        if top_user:
            save_spotlight_user(top_user[0])
