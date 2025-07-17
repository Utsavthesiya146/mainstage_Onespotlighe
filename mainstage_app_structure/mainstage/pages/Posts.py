import streamlit as st
from datetime import datetime
import os
from utils.database import save_post, get_all_posts

st.set_page_config(page_title="Community Posts", layout="centered")
st.title("🌍 Community Posts")
st.caption("Share your thoughts with the MainStage world!")

# 🔐 Check if user is logged in
if "user" not in st.session_state:
    st.warning("Please sign in to post and view content.")
    st.stop()

user = st.session_state["user"]

# 🎯 Post submission form
with st.form("post_form", clear_on_submit=True):
    st.subheader("✍️ Create a Post")
    content = st.text_area("Your message", max_chars=280, placeholder="What's on your mind?", height=100)
    image = st.file_uploader("Upload an optional image", type=["png", "jpg", "jpeg"])
    submitted = st.form_submit_button("📤 Post")

    if submitted:
        image_url = None
        if image:
            # 📁 Save image to 'uploads/' folder
            os.makedirs("uploads", exist_ok=True)
            filename = f"uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}_{image.name}"
            with open(filename, "wb") as f:
                f.write(image.read())
            image_url = filename

        if content.strip() != "":
            save_post(user_id=user["id"], username=user["name"], content=content.strip(), image_url=image_url)
            st.success("✅ Post uploaded successfully!")
        else:
            st.error("Post content cannot be empty.")

# 📰 Divider + Recent Posts Section
st.divider()
st.subheader("📰 Recent Posts")

posts = get_all_posts()

if not posts:
    st.info("No posts yet. Be the first to share something!")
else:
    for post in posts:
        st.markdown(f"**🧑 {post['username']}** — 🕒 {post['timestamp']}")
        st.markdown(f"{post['content']}")
        if post["image_url"] and os.path.exists(post["image_url"]):
            st.image(post["image_url"], use_container_width=True)
        st.markdown("---")
