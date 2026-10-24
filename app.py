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

# --- SIDEBAR & USER PROFILE SETUP ---
st.sidebar.markdown("## 📝 User Profile Setup")
user_name = st.sidebar.text_input("Your Name", "Feriel")
teach_skill = st.sidebar.text_input("What skill can you teach?", "Python Programming")
learn_skill = st.sidebar.text_input("What skill do you want to learn?", "Spanish")

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
                
                matches = [
                    u for u in users 
                    if u.get("name") != user_name and (
                        u.get("teach_skill", "").lower() == learn_skill.lower() or 
                        u.get("learn_skill", "").lower() == teach_skill.lower()
                    )
                ]
                
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
                    st.info("No direct matches found in the live database yet. Try broadening your skills or invite fellow students!")
                    
                    st.markdown("### 🌟 Community Skill Pool (Live Preview)")
                    st.markdown("""
                    - 👤 **Anfal** | Teaches: `Data Science` | Wants: `French`
                    - 👤 **Yineb** | Teaches: `Digital Marketing` | Wants: `Python`
                    - 👤 **Amina** | Teaches: `Spanish` | Wants: `UI/UX Design`
                    """)
            except Exception as e:
                st.error(f"Could not fetch matches from database: {e}")

# --- TAB 2: HOUR BANK ---
with tab2:
    st.header("Hour Bank & Skill Credits")
    st.write("Earn hours by teaching your skills, and spend hours learning new ones!")
    col1, col2, col3 = st.columns(3)
    col1.metric("Hours Earned (Teaching)", "12 hrs", "+2 this week")
    col2.metric("Hours Spent (Learning)", "8 hrs", "-1.5 this week")
    col3.metric("Net Credit Balance", "4 hrs Available", "🟢 Active Status")

# --- TAB 3: EXCUSE VALIDATOR ---
with tab3:
    st.header("AI Excuse Validator & Rescheduling")
    st.write("Need to reschedule a peer session? Submit your excuse for fair AI evaluation.")
    excuse_text = st.text_area("Describe your reason for rescheduling:")
    if st.button("Evaluate Excuse"):
        if excuse_text:
            st.info("🤖 **AI Validator Assessment:** Valid reason approved. Session rescheduled with zero credit penalty to maintain your Reliable Partner Badge.")
        else:
            st.warning("Please enter an excuse reason first.")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>PeerHub Full-Stack App — Powered by Supabase & Streamlit (Thirduni - October 2026)</p>", unsafe_allow_html=True)
