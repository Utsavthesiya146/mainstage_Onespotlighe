from datetime import datetime, timedelta
from utils.database import get_spotlight_user

# ⏳ Time left until spotlight rotates (24h cycle)
def get_remaining_time():
    _, started_at = get_spotlight_user()

    if not started_at:
        return "24:00:00"

    started_time = datetime.fromisoformat(started_at)
    now = datetime.now()

    # ⏱️ Calculate time left
    end_time = started_time + timedelta(hours=24)
    remaining = end_time - now

    if remaining.total_seconds() < 0:
        return "00:00:00"

    hours, remainder = divmod(int(remaining.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours:02}:{minutes:02}:{seconds:02}"
