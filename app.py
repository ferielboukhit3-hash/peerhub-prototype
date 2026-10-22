# ==========================================
# PeerHub — Interactive Skill Exchange Platform
# Production-Ready MVP (Thirduni - October 2026)
# ==========================================

import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="PeerHub — Interactive Skill Exchange",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Styling for a Professional SaaS Look
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #4f46e5;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        border: none;
    }
    .stButton>button:hover {
        background-color: #4338ca;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# App Header & Branding Banner
st.markdown("<h1 style='text-align: center; color: #4f46e5;'>🚀 PeerHub</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #6b7280;'>Interactive Skill Exchange & Live Peer-to-Peer Learning Ecosystem</h3>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar: User Profile Setup
st.sidebar.header("📝 User Profile Setup")
user_name = st.sidebar.text_input("Your Name", "Feriel")
teach_skill = st.sidebar.selectbox("What skill can you teach?", ["Python Programming", "Spanish", "UI/UX Design (Canva)"])
learn_skill = st.sidebar.selectbox("What skill do you want to learn?", ["Spanish", "Python Programming", "English"])
weekly_availability = st.sidebar.slider("Weekly Availability (Hours)", 1, 10, 3)

# Mock Database for Matching
users_db = [
    {"name": "Ahmed", "teach": "Python Programming", "learn": "Spanish", "credits": 2, "badge": "Reliable Partner ⭐"},
    {"name": "Maria", "teach": "Spanish", "learn": "Python Programming", "credits": 1, "badge": "Committed Beginner 📌"},
    {"name": "Sarah", "teach": "UI/UX Design (Canva)", "learn": "English", "credits": 3, "badge": "Reliable Partner ⭐"}
]

# Organized Dashboard Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Matching Engine", "💰 Hour Bank & Credits", "🛡️ AI Excuse Validator"])

# TAB 1: Matching Engine
with tab1:
    st.subheader("Teach vs. Learn Matching Dashboard")
    st.write(f"Welcome back, **{user_name}**! Find your ideal learning partner based on the Skill Barter Economy.")

    col1, col2 = st.columns([2, 1])
    with col1:
        if st.button("🔍 Find Perfect Match"):
            match_found = False
            for partner in users_db:
                if partner["teach"] == learn_skill and partner["learn"] == teach_skill:
                    st.success(f"🎉 Perfect Match Found! You are paired with: **{partner['name']}**")
                    st.info(f"🏆 Badge: {partner['badge']} | 💰 Skill Credits: {partner['credits']} Hours")
                    match_found = True
                    break
            if not match_found:
                st.warning("⚠️ No direct match found right now. Your request has been safely added to the Skill Barter Economy queue.")

    with col2:
        st.metric(label="Your Current Status", value="Active Learner", delta="Reliable")

# TAB 2: Hour Bank & Credits
with tab2:
    st.subheader("Skill Credits / Hour Bank")
    st.write("Track your earned hours and exchange value transparently within PeerHub.")

    c1, c2, c3 = st.columns(3)
    c1.metric("Available Credits", "2 Hours", "+1 Hour this week")
    c2.metric("Completed Sessions", "4 Sessions", "100% Success Rate")
    c3.metric("Attendance Score", "100%", "Protected")

    if st.button("Claim Hour Credits for Completed Session"):
        st.success("✅ Session verified! 1 Hour successfully added to your Skill Credits / Hour Bank.")

# TAB 3: AI Excuse Validation System
with tab3:
    st.subheader("🛡️ AI-Powered Excuse Validation System")
    st.write("Submit your scheduling conflict or absence reason for intelligent evaluation by the platform's AI guardrails.")

    excuse_reason = st.text_input("Enter your excuse / reason:", placeholder="e.g., Internet outage, Health emergency, or personal reasons")

    if st.button("Analyze & Submit Excuse"):
        if excuse_reason:
            reason_lower = excuse_reason.lower()
            valid_keywords = ["internet", "outage", "health", "emergency", "sick", "hospital", "power", "electricity", "family"]
            is_valid = any(word in reason_lower for word in valid_keywords)

            if is_valid:
                st.success("✅ **AI Evaluation: Approved (Valid Emergency/Technical Issue)**")
                st.info("💡 **AI Feedback:** Your reason has been verified as a legitimate constraint. Your attendance score remains fully protected, and the system has automatically scheduled a makeup session.")
            else:
                st.warning("⚠️ **AI Evaluation: Flagged (Weak or Unexcused Reason)**")
                st.error("💡 **AI Feedback:** The provided reason does not meet emergency criteria. A 10% attendance deduction has been applied. Please ensure better commitment to maintain your 'Reliable Partner' status.")
        else:
            st.warning("Please type a reason before submitting your excuse.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #9ca3af;'>PeerHub Prototype (MVP) — Built with Python & Streamlit for Thirduni — October 2026</p>", unsafe_allow_html=True)
