import os
import uuid

# 📁 Ensure profile picture directory exists
UPLOAD_DIR = os.path.join("assets", "profile_pics")
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_image(uploaded_file):
    if uploaded_file is None:
        return None

    # 📸 Generate unique filename
    ext = uploaded_file.name.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    # 🛣️ Full path
    save_path = os.path.join(UPLOAD_DIR, filename)

    # 💾 Save image
    with open(save_path, "wb") as f:
        f.write(uploaded_file.read())

    return save_path
