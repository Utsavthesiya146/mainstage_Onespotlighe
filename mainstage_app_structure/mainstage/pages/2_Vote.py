import streamlit as st
from utils.database import get_all_users, save_vote

st.title("🗳️ Vote for Today's Spotlight")

users = get_all_users()

if not users:
    st.info("No profiles available yet. Ask someone to create one from the Profile page.")
else:
    voter_name = st.text_input("👤 Enter the name of the person you want to vote for")
    selected = st.radio("👑 Who do you want to vote for?", [f"{u[1]} (ID: {u[0]})" for u in users])

    if st.button("✅ Submit Vote"):
        if not voter_name.strip():
            st.error("Please enter your name before voting.")
        else:
            voted_user_id = int(selected.split("ID: ")[1].replace(")", ""))
            save_vote(voter_name.strip(), voted_user_id)
            st.success(f"✅ Vote casted for {selected.split(' (')[0]}!")
