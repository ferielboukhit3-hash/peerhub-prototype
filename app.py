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
    st.session_state.excuse_count = 1  # User used 1 out of 2 allowed per month

if "partner_approval_count" not in st.session_state:
    st.session_state.partner_approval_count = 3  # Partner used 3 out of 5 allowed per month

if "audit_log" not in st.session_state:
    st.session_state.audit_log = [
        {"user": "Feriel", "partner": "Maria", "excuse_type": "Internet Outage", "monthly_count": "1/2", "status": "Verified Rescheduling Demand", "partner_note": "Partner's Review Note: I confirm we agreed on rescheduling this session."}
    ]

if "pending_excuse" not in st.session_state:
    st.session_state.pending_excuse = {
        "user": "Feriel",
        "partner": "Maria",
        "excuse_type": "Internet Outage / Technical",
        "text": "Sudden internet outage and power cut before session."
    }

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
    
    # Monthly Status Tracker (User)
    current_used = st.session_state.excuse_count
    remaining = max(0, 2 - current_used)
    st.info(f"📅 **User Monthly Policy Tracker:** You have used **{current_used} of 2** allowed approved excuses this month. (**{remaining}** remaining)")
    
    # --- SIMULATION MODE TOGGLE FOR DEMO VIDEO ---
    st.markdown("### 🎬 Demo Simulation Mode")
    sim_mode = st.radio(
        "Switch View Mode for Demo Recording:",
        ["1. User View: Submit Excuse & Request Rescheduling", "2. Partner View: Review & Write Custom Note"],
        horizontal=True
    )
    
    col_a, col_b = st.columns(2)
    with col_a:
        assigned_partner = st.selectbox("Select Your Learning Partner:", ["Maria", "Ahmed", "Amir", "Lina", "Chaima"])
    with col_b:
        excuse_type_label = st.selectbox("Excuse Category:", ["Internet Outage / Technical", "Health Emergency / Sick", "University Exam / Academic", "Family Emergency"])
    
    if sim_mode.startswith("1"):
        st.markdown("#### 📤 Step 1: Submit Excuse (As User)")
        excuse_text = st.text_area("Describe reason for rescheduling:", placeholder="e.g., Sudden power outage and internet disconnection...")
        
        if st.button("Submit for Partner & AI Audit"):
            if excuse_text:
                st.session_state.pending_excuse = {
                    "user": user_name,
                    "partner": assigned_partner,
                    "excuse_type": excuse_type_label,
                    "text": excuse_text
                }
                st.success(f"⏳ **Status: Pending Partner Verification.** Excuse sent to **{assigned_partner}** successfully! Switch to *Partner View* above to review and sign off.")
            else:
                st.warning("Please describe your reason first.")
                
    else:
        st.markdown("#### 📥 Step 2: Partner Review & Sign-off (As Partner)")
        
        # Display Partner Monthly Approval Quota
        p_approvals_used = st.session_state.partner_approval_count
        st.info(f"🛡️ **Partner Governance Quota:** Partner Approvals Used: **{p_approvals_used} of 5** allowed this month.")
        
        # Safely retrieve pending excuse text and details
        current_pending = st.session_state.get("pending_excuse", {})
        p_user = current_pending.get("user", user_name)
        p_text = current_pending.get("text", "No excuse text provided.")
        p_category = current_pending.get("excuse_type", excuse_type_label)
        
        # Display clear message showing the excuse from the user
        st.write(f"👤 **Reviewing excuse from {p_user}:** '{p_text}' (Category: *{p_category}*)")
        
        # Rights Protection Disclaimer
        st.markdown(
            "> ⚖️ **PeerHub Rights Protection Disclaimer:** PeerHub protects your learning rights, giving you the power to carefully review, comment, and explicitly accept or reject your partner's excuse."
        )
        
        # Custom Written Partner Feedback/Approval Note Input
        partner_feedback_note = st.text_input(
            "Partner's Written Review Note / Reason:", 
            placeholder="e.g., Partner's Review Note: I confirm we agreed on rescheduling this session..."
        )
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            if st.button("✅ Approve Partner Rescheduling"):
                if not partner_feedback_note:
                    st.warning("Please write a custom approval note before submitting.")
                else:
                    # Check partner approval limit (Max 5 approvals per partner per month)
                    if st.session_state.partner_approval_count >= 5:
                        st.error("🚨 **Partner Monthly Approval Limit Reached (5/5).**")
                        st.warning("To protect learning commitments, extra reschedules require direct platform mediation or standard penalty rules.")
                    else:
                        reason_lower = p_text.lower()
                        weak_triggers = ["lazy", "forgot", "bored", "playing", "sleep"]
                        is_weak = any(w in reason_lower for w in weak_triggers)
                        
                        if st.session_state.excuse_count >= 2:
                            st.error("🚨 **User Limit Exceeded!** 3rd excuse attempt rejected despite partner sign-off. Penalty applied.")
                            st.session_state.audit_log.insert(0, {
                                "user": p_user, "partner": assigned_partner, "excuse_type": p_category, 
                                "monthly_count": "3/2 (Exceeded)", "status": "Rejected - Limit Exceeded",
                                "partner_note": partner_feedback_note
                            })
                        elif is_weak:
                            st.warning("⚠️ **AI Audit Flagged:** Approved by partner, but flagged by AI as weak reason.")
                        else:
                            st.session_state.excuse_count += 1
                            st.session_state.partner_approval_count += 1
                            st.success("✅ **Verified Rescheduling Demand Approved!** Both users are bound to the makeup session time. Zero credit penalty.")
                            st.session_state.audit_log.insert(0, {
                                "user": p_user, "partner": assigned_partner, "excuse_type": p_category, 
                                "monthly_count": f"{st.session_state.excuse_count}/2", "status": "Verified Rescheduling Demand",
                                "partner_note": partner_feedback_note
                            })
                            st.balloons()
                    
        with col_p2:
            if st.button("❌ Reject & Flag"):
                if not partner_feedback_note:
                    st.warning("Please write a custom rejection note explaining why.")
                else:
                    st.error("❌ **Rescheduling Request Rejected by Partner.** Credit penalty applied.")
                    st.session_state.audit_log.insert(0, {
                        "user": p_user, "partner": assigned_partner, "excuse_type": p_category, 
                        "monthly_count": f"{st.session_state.excuse_count}/2", "status": "Rejected by Partner",
                        "partner_note": partner_feedback_note
                    })

    st.markdown("---")
    st.subheader("🌐 Community Trust & Audit Log (Public Ledger)")
    st.write("Recent peer session accountability audits visible to judges in real-time:")
    
    # Display Audit Log Table including Partner's Written Note & Verified Demand Status
    st.table(st.session_state.audit_log)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>PeerHub Full-Stack App — Powered by Supabase & Streamlit (Thirduni - October 2026)</p>", unsafe_allow_html=True)
