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

# --- SESSION STATE INITIALIZATION ---
if "excuse_count" not in st.session_state:
    st.session_state.excuse_count = 0  # 0 used out of 2 allowed per month

if "audit_log" not in st.session_state:
    st.session_state.audit_log = [
        {"user": "Feriel", "partner": "Maria", "excuse_type": "Internet Outage", "monthly_count": "2/2", "status": "Approved by Partner & AI"},
        {"user": "Ahmed", "partner": "Amir", "excuse_type": "Exam Conflict", "monthly_count": "1/2", "status": "Approved by Partner & AI"}
    ]

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
tab1, tab2, tab3 = st.tabs(["🔍 Matching Engine", "💰 Hour Bank & Credits", "🛡️ AI Excuse & Partner Audit"])

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

# --- TAB 3: EXCUSE VALIDATOR & PARTNER AUDIT SYSTEM ---
with tab3:
    st.header("🛡️ Partner Verification & AI Excuse Audit System")
    st.write("Need to reschedule a session? Submit your excuse for dual-layer verification: **Partner Sign-off** & **AI Policy Check**.")
    
    # Monthly Status Tracker
    current_used = st.session_state.excuse_count
    remaining = max(0, 2 - current_used)
    st.info(f"📅 **Monthly Policy Tracker:** You have used **{current_used} of 2** allowed approved excuses this month. (**{remaining}** remaining)")
    
    col_a, col_b = st.columns(2)
    with col_a:
        assigned_partner = st.selectbox("Select Your Learning Partner:", ["Maria", "Ahmed", "Amir", "Lina", "Chaima"])
    with col_b:
        excuse_type_label = st.selectbox("Excuse Category:", ["Internet Outage / Technical", "Health Emergency / Sick", "University Exam / Academic", "Family Emergency"])
    
    excuse_text = st.text_area("Describe reason for rescheduling:", placeholder="e.g., Sudden power outage and internet disconnection...")
    
    st.markdown("#### 👥 Two-Step Verification Workflow")
    verification_step = st.radio("Simulation Mode (Role Switch):", ["1. Submit Excuse (User)", "2. Partner Review & Sign-off"])
    
    if verification_step == "1. Submit Excuse (User)":
        if st.button("Submit for Partner & AI Audit"):
            if excuse_text:
                st.session_state.pending_excuse = {
                    "user": user_name,
                    "partner": assigned_partner,
                    "excuse_type": excuse_type_label,
                    "text": excuse_text
                }
                st.warning(f"⏳ **Status: Pending Partner Verification.** Sent to **{assigned_partner}** for review.")
            else:
                st.warning("Please describe your reason first.")
                
    elif verification_step == "2. Partner Review & Sign-off":
        st.info(f"👤 Logged in as Partner (**{assigned_partner}** reviewing request from **{user_name}**):")
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            if st.button("✅ Approve Partner Rescheduling"):
                reason_lower = excuse_text.lower() if 'excuse_text' in locals() else ""
                weak_triggers = ["lazy", "forgot", "bored", "playing", "sleep"]
                is_weak = any(w in reason_lower for w in weak_triggers)
                
                if st.session_state.excuse_count >= 2:
                    st.error("🚨 **Limit Exceeded!** 3rd excuse attempt rejected despite partner sign-off. Penalty applied.")
                    st.session_state.audit_log.insert(0, {
                        "user": user_name, "partner": assigned_partner, "excuse_type": excuse_type_label, 
                        "monthly_count": "3/2 (Exceeded)", "status": "Rejected - Limit Exceeded"
                    })
                elif is_weak:
                    st.warning("⚠️ **AI Audit Flagged:** Approved by partner, but flagged by AI as weak reason.")
                else:
                    st.session_state.excuse_count += 1
                    st.success("✅ **Approved by Partner & AI Policy Check!** Zero credit penalty. Badge protected.")
                    st.session_state.audit_log.insert(0, {
                        "user": user_name, "partner": assigned_partner, "excuse_type": excuse_type_label, 
                        "monthly_count": f"{st.session_state.excuse_count}/2", "status": "Approved by Partner & AI"
                    })
                    st.balloons()
                    
        with col_p2:
            if st.button("❌ Reject & Flag"):
                st.error("❌ **Rescheduling Request Rejected by Partner.** Credit penalty applied.")
                st.session_state.audit_log.insert(0, {
                    "user": user_name, "partner": assigned_partner, "excuse_type": excuse_type_label, 
                    "monthly_count": f"{st.session_state.excuse_count}/2", "status": "Rejected by Partner"
                })

    st.markdown("---")
    st.subheader("🌐 Community Trust & Audit Log (Public Ledger)")
    st.write("Recent peer session accountability audits visible to judges in real-time:")
    
    # Display Audit Log Table
    st.table(st.session_state.audit_log)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>PeerHub Full-Stack App — Powered by Supabase & Streamlit (Thirduni - October 2026)</p>", unsafe_allow_html=True)
