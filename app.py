# ==========================================
# PeerHub - Interactive Skill Exchange Prototype (MVP)
# ==========================================

import streamlit as st

st.set_page_config(page_title="PeerHub Prototype", page_icon="🚀", layout="centered")

# Main Title & Subtitle
st.title("🚀 PeerHub — Interactive Skill Exchange")
st.subheader("Skill Barter Economy & Live Peer-to-Peer Learning")

st.markdown("---")

# Sidebar: User Profile & Input
st.sidebar.header("📝 User Profile Setup")
user_name = st.sidebar.text_input("Your Name", "Feriel")
teach_skill = st.sidebar.selectbox("What skill can you teach?", ["Python Programming", "Spanish", "UI/UX Design (Canva)"])
learn_skill = st.sidebar.selectbox("What skill do you want to learn?", ["Spanish", "Python Programming", "English"])
weekly_availability = st.sidebar.slider("Weekly Availability (Hours)", 1, 10, 3)

st.write(f"### Welcome back, {user_name}! Here is your Teach vs. Learn matching dashboard:")

# Mock Database with advanced terms
users_db = [
    {"name": "Ahmed", "teach": "Python Programming", "learn": "Spanish", "credits": 2, "badge": "Reliable Partner ⭐"},
    {"name": "Maria", "teach": "Spanish", "learn": "Python Programming", "credits": 1, "badge": "Committed Beginner 📌"},
    {"name": "Sarah", "teach": "UI/UX Design (Canva)", "learn": "English", "credits": 3, "badge": "Reliable Partner ⭐"}
]

# Action Buttons & Matching Engine
col1, col2 = st.columns(2)

with col1:
    if st.button("🔍 Find Match"):
        match_found = False
        for partner in users_db:
            if partner["teach"] == learn_skill and partner["learn"] == teach_skill:
                st.success(f"🎉 Perfect Match Found! You are paired with: {partner['name']}")
                st.info(f"🏆 Badge: {partner['badge']} | 💰 Skill Credits / Hour Bank: {partner['credits']} Hours")
                match_found = True
                break
        if not match_found:
            st.warning("⚠️ No direct match found right now. Your request has been safely added to the Skill Barter Economy queue.")

with col2:
    if st.button("Claim Hour Credits"):
        st.success("✅ Session completed! 1 Hour added to your Skill Credits / Hour Bank.")

st.markdown("---")

# Excuse Management Section
st.subheader("🛡️ Excuse Management System")
excuse_reason = st.text_input("Submit valid excuse (if missing a scheduled live session):", placeholder="e.g., Internet outage / Health emergency")
if st.button("Submit Valid Excuse"):
    if excuse_reason:
        st.info("⚠️ Excuse submitted to the platform review system. Your attendance score remains protected.")
    else:
        st.warning("Please type a reason before submitting your excuse.")

st.markdown("---")
st.caption("PeerHub Prototype (MVP) — Built for Thirduni — October 2026")
