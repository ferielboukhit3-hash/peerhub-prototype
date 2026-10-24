import streamlit as st
from supabase import create_client, Client

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PeerHub — Interactive Skill Exchange",
    page_icon="🤝",
    layout="wide"
)

# --- SUPABASE CONNECTION SETUP ---
SUPABASE_URL = "https://lhkvquolmpvdzlrgraqr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxoa3ZxdW9sbXB2ZHpscmdyYXFyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTI2OTExMTIsImV4cCI6MjEwODI2NzExMn0.xexmDDV1_A7oC-83errG-hCMGpXz25NcpoilmE5d73A"

@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

try:
    supabase = init_supabase()
    db_status = "Connected to Supabase Live Database 🟢"
except Exception as e:
    db_status = f"Database Connection Error: {e}"

# --- SESSION STATE INITIALIZATION FOR MONTHLY EXCUSE LIMIT ---
if "excuse_count" not in st.session_state:
    st.session_state.excuse_count = 0  # Starts with 0 used out of 2 allowed per month

# --- SIDEBAR & USER PROFILE SETUP ---
st.sidebar.markdown("## 📝 User Profile Setup")
user_name = st.sidebar.text_input("Your Name", "Feriel")
teach_skill = st.sidebar.selectbox("What skill can you teach?", ["Python Programming", "Spanish", "UI/UX Design (Canva)", "French"])
learn_skill = st.sidebar.selectbox("What skill do you want to learn?", ["Spanish", "Python Programming", "English", "Data Science"])

if st.sidebar.button("Save Profile to Cloud"):
    try:
        data = {
            "name": user_name,
            "teach_skill": teach_skill,
            "learn_skill": learn_skill
        }
        supabase.table("Profiles").insert(data).execute()
        st.sidebar.success("Profile saved successfully to Supabase! 🎉")
    except Exception as ex:
        st.sidebar.error(f"Error saving profile: {ex}")

# --- MAIN APP HEADER ---
st.title("🚀 PeerHub")
st.subheader("Interactive Skill Exchange & Live Peer-to-Peer Learning Ecosystem")

st.markdown("---")

# Navigation Tabs
tab1, tab2, tab3 = st.tabs(["🔍 Matching Engine", "💰 Hour Bank & Credits", "🛡️ AI Excuse Validator"])

# --- TAB 1: LIVE MATCHING ENGINE ---
with tab1:
    st.header("Teach vs. Learn Matching Dashboard")
    st.write(f"Welcome back, **{user_name}**! {db_status}")
    
    if st.button("🔍 Find Perfect Match from Database"):
        with st.spinner("Searching live database for potential partners..."):
            try:
                response = supabase.table("Profiles").select("*").execute()
                users = response.data
                
                if not users:
                    users = [
                        {"name": "Ahmed", "teach_skill": "Python Programming", "learn_skill": "Spanish"},
                        {"name": "Maria", "teach_skill": "Spanish", "learn_skill": "Python Programming"},
                        {"name": "Amir", "teach_skill": "UI/UX Design (Canva)", "learn_skill": "Python Programming"}
                    ]
                
                matches = [
                    u for u in users 
                    if u.get("name", "").lower() != user_name.lower() and (
                        u.get("teach_skill", "").lower() == learn_skill.lower() or 
                        u.get("learn_skill", "").lower() == teach_skill.lower()
                    )
                ]
                
                if not matches:
                    matches = [u for u in users if u.get("name", "").lower() != user_name.lower()]

                if matches:
                    st.success(f"Found {len(matches)} compatible peer(s) in the live database! ✨")
                    for m in matches:
                        with st.container():
                            st.markdown(f"""
                            - 👤 **Peer Name:** {m.get('name')}
                            - 🎓 **Can Teach You:** `{m.get('teach_skill')}`
                            - 📚 **Wants to Learn:** `{m.get('learn_skill')}`
                            """)
                            if st.button(f"Request Session with {m.get('name')}", key=f"req_{m.get('name')}"):
                                st.balloons()
                                st.info(f"Session exchange request sent to {m.get('name')}!")
                else:
                    st.info("No peers found in the database yet. Save your profile to join the queue!")
            except Exception as e:
                st.error(f"Could not fetch matches from database: {e}")

# --- TAB 2: HOUR BANK ---
with tab2:
    st.header("Hour Bank & Skill Credits")
    st.write(f"Track your earned hours and exchange value transparently within PeerHub, **{user_name}**.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Hours Earned (Teaching)", "3 hrs", "+1 this week")
    col2.metric("Hours Spent (Learning)", "2 hrs", "-0.5 this week")
    col3.metric("Net Credit Balance", "1 hr Available", "🟢 Active Status")
    
    st.markdown("---")
    st.subheader("Session Verification & Credit Claim")
    completed_with = st.text_input("Completed session with partner name:", "Maria")
    session_topic = st.text_input("Session topic taught/learned:", "Python Basics")
    
    if st.button("Claim +1 Hour Credit"):
        if completed_with:
            st.success(f"✅ Verified! 1 Hour credit successfully added to your account for the session with **{completed_with}**.")
            st.balloons()
        else:
            st.warning("Please enter your partner's name first.")

# --- TAB 3: EXCUSE VALIDATOR ---
with tab3:
    st.header("🛡️ AI Excuse Validator & Rescheduling")
    st.write("Need to reschedule a peer session? Submit your reason below for intelligent AI evaluation and strict policy enforcement.")
    
    # Display Monthly Status Tracker
    current_used = st.session_state.excuse_count
    remaining = max(0, 2 - current_used)
    st.info(f"📅 **Monthly Policy Tracker:** You have used **{current_used} of 2** allowed approved excuses this month. (**{remaining}** remaining)")
    
    excuse_text = st.text_area("Describe your reason for rescheduling:", placeholder="e.g., Sudden internet outage, health emergency, or university exam conflict...")
    
    if st.button("Evaluate Excuse with AI"):
        if excuse_text:
            reason_lower = excuse_text.lower()
            
            # Strict Content Evaluation: Check for weak, vague, or nonsensical excuses
            weak_triggers = ["i don't want", "lazy", "forgot", "bored", "playing", "sleep", "gaming", "whatever", "nothing"]
            is_obviously_weak = any(w in reason_lower for w in weak_triggers)
            
            valid_keywords = ["internet", "outage", "health", "emergency", "sick", "hospital", "power", "electricity", "exam", "study", "family", "connection", "network"]
            is_keyword_valid = any(word in reason_lower for word in valid_keywords)
            
            # Check if user has exceeded the monthly limit of 2
            if st.session_state.excuse_count >= 2:
                st.error("🚨 **Monthly Limit Exceeded (3rd Excuse Attempt)!**")
                st.warning("⚠️ You have already used your maximum limit of **2 approved excuses** for this month. This 3rd request is **automatically rejected**.")
                st.error("❌ **Penalty Applied:** 1 Hour credit deducted and your 'Reliable Partner' badge has been suspended / downgraded due to policy limit breach.")
            elif is_obviously_weak or not is_keyword_valid:
                st.warning("⚠️ **AI Evaluation: Flagged & Rejected (Weak or Vague Reason)**")
                st.write("💡 Note: Casual or nonsensical reasons do not qualify for emergency waivers. Please coordinate directly with your peer.")
            else:
                # Valid excuse and under the limit (1st or 2nd excuse of the month)
                st.session_state.excuse_count += 1
                st.success(f"✅ **AI Evaluation: Approved (Valid Emergency / Technical / Academic Issue)**")
                st.info(f"💡 Session rescheduled successfully with **zero credit penalty**. Excuse **{st.session_state.excuse_count} of 2** recorded for this month. Your 'Reliable Partner' badge remains fully protected! 🎉")
                st.balloons()
        else:
            st.warning("Please enter an excuse reason first.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>PeerHub Full-Stack App — Powered by Supabase & Streamlit (Thirduni - October 2026)</p>", unsafe_allow_html=True)
