import streamlit as st
import os
import sys
from utils.sqlite_config import create_posts_table
import streamlit as st
import os
from utils.database import create_user, get_user_by_name


# Call this once to ensure table exists
create_posts_table()

# 🔧 Ensure local modules are discoverable
sys.path.append(os.path.dirname(__file__))

# ✅ Import local utilities
# from utils.database import init_db
from utils.timer import get_remaining_time
from utils.spotlight import rotate_spotlight

# ✅ Initialize database (only first time needed)
# init_db()

# ✅ Automatically rotate spotlight user if 24hrs passed
rotate_spotlight()

# ✅ Page settings
st.set_page_config(
    page_title="MainStage",
    page_icon="🎭",
    layout="wide"
)

# ✅ Logo
st.image("D:\\mainstage_app_structure\\mainstage\\assets\\logo.png", width=120)

# ✅ Main Title
st.markdown("<h1 style='color:#FFD700;'>🎭 Welcome to MainStage</h1>", unsafe_allow_html=True)

# ✅ Sidebar Menu 👇👇👇 ADD THIS SECTION
st.sidebar.title("📱 MainStage Menu")
st.sidebar.page_link("pages/1_Home.py", label="🏠 Home")
st.sidebar.page_link("pages/2_Vote.py", label="🗳️ Vote")
st.sidebar.page_link("pages/3_Profile.py", label="🧑‍🎤 Profile")
st.sidebar.page_link("pages/4_Leaderboard.py", label="🏆 Leaderboard")


# ✅ Description
st.markdown("This is your spotlight moment on the internet – create your profile, vote for others, and shine!")

# ✅ Instructions with style
st.markdown("""
<style>
.instructions {
    background-color: #2E2E48;
    padding: 1rem;
    border-radius: 8px;
    color: white;
    font-size: 16px;
    margin-top: 20px;
}
</style>
<div class='instructions'>
<ul>
    <li>✨ instructions :</li>
    <li>👤 Go to <b>Profile</b> page and create your identity.</li>
    <li>🔧 Go to <b>Profile</b> page to edit your identity anytime.</li>
    <li>🗳️ Visit <b>Vote</b> to support your favorite profile.</li>
    <li>🌟 The most voted user is crowned the spotlight for 24 hours!</li>
</ul>
</div>
""", unsafe_allow_html=True)

# ✅ Countdown timer
remaining = get_remaining_time()
st.markdown(f"⏳ Time left until next spotlight: **{remaining}**")

st.set_page_config(page_title="Sign In", layout="centered")
st.title("🔐 Sign In & Log In MainStage")


if "user" in st.session_state:
    st.success(f"✅ You're already signed in as {st.session_state['user']['name']}")
    st.switch_page("pages/1_Home.py")


username = st.text_input("👤 Enter your name")


user = get_user_by_name(username.strip()) if username.strip() else None

if user:
    st.info(f"👋 Hello {user[1]}! You already have an account.")
    if st.button("➡️ Continue to Home"):
        st.session_state["user"] = {
            "id": user[0],
            "name": user[1],
            "bio": user[2],
            "image_url": user[3]
        }
        st.success("✅ Signed in successfully!")
        st.switch_page("pages/1_Home.py")
else:
    if username.strip() != "":
        st.warning("🤔 This name is not registered.")
        create_new = st.radio("Do you want to create a new account?", ["No", "Yes"])

        if create_new == "Yes":
            bio = st.text_area("📝 Enter your short bio")
            image = st.file_uploader("📸 Upload profile picture (optional)", type=["png", "jpg", "jpeg"])
            
            if st.button("🚀 Create Account"):
                image_path = None
                if image:
                    os.makedirs("uploads", exist_ok=True)
                    image_path = f"uploads/{username.replace(' ', '_')}_{image.name}"
                    with open(image_path, "wb") as f:
                        f.write(image.read())

                create_user(username.strip(), bio.strip(), image_path)
                new_user = get_user_by_name(username.strip())
                st.session_state["user"] = {
                    "id": new_user[0],
                    "name": new_user[1],
                    "bio": new_user[2],
                    "image_url": new_user[3]
                }
                st.success("🎉 Account created successfully!")
                st.switch_page("pages/1_Home.py")
        else:
            st.info("🔁 Please enter your registered name to continue.")