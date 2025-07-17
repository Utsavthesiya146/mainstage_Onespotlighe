import streamlit as st
import os
import uuid
from utils.database import create_user, get_all_users, update_user
from utils.uploads import save_uploaded_image

st.title("🧑‍🎤 Your MainStage Profile")

# 🔄 Step 1: Select existing profile (for editing)
users = get_all_users()
user_names = [f"{u[1]} (ID: {u[0]})" for u in users]
user_dict = {f"{u[1]} (ID: {u[0]})": u for u in users}

selected_profile = st.selectbox("🔍 Select your profile (to edit or view)", ["➕ Create New"] + user_names)

if selected_profile != "➕ Create New":
    selected_user = user_dict[selected_profile]
    user_id = selected_user[0]
    name = st.text_input("📝 Edit your name", selected_user[1])
    bio = st.text_area("📖 Edit your bio", selected_user[2])
    current_image = selected_user[3]

    if current_image:
        st.image(current_image, width=150)

    new_image = st.file_uploader("📸 Change your profile picture (optional)", type=["png", "jpg", "jpeg"])

    if st.button("💾 Update Profile"):
        image_path = current_image  # default
        if new_image:
            img_folder = "assets/profile_pics"
            os.makedirs(img_folder, exist_ok=True)
            ext = new_image.name.split(".")[-1]
            filename = f"{uuid.uuid4()}.{ext}"
            image_path = os.path.join(img_folder, filename)
            with open(image_path, "wb") as f:
                f.write(new_image.read())

        update_user(user_id, name.strip(), bio.strip(), image_path)
        st.success("✅ Profile updated successfully!")

else:
    # ➕ New profile creation
    name = st.text_input("📝 Enter your name")
    bio = st.text_area("📖 Tell us something about yourself")
    image = st.file_uploader("📸 Upload your profile picture (PNG/JPG)", type=["png", "jpg", "jpeg"])

    if st.button("🚀 Create Profile"):
        if not name.strip() or not bio.strip():
            st.error("Please fill in both name and bio.")
        else:
            image_path = None
            if image:
                img_folder = "assets/profile_pics"
                os.makedirs(img_folder, exist_ok=True)
                ext = image.name.split(".")[-1]
                filename = f"{uuid.uuid4()}.{ext}"
                image_path = os.path.join(img_folder, filename)
                with open(image_path, "wb") as f:
                    f.write(image.read())

            create_user(name.strip(), bio.strip(), image_path)
            st.success("🎉 Profile created successfully!")
            
            image = st.file_uploader("📸 Upload image", type=["jpg", "png"])
            image_path = save_uploaded_image(image)
