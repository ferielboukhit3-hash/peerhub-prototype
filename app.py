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
    st.session_state.excuse_count = 1

if "partner_approval_count" not in st.session_state:
    st.session_state.partner_approval_count = 3

if "user_credits" not in st.session_state:
    st.session_state.user_credits = 5

if "completed_sessions" not in st.session_state:
    st.session_state.completed_sessions = 4

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = {
        "Maria": [
            {"sender": "Maria", "text": "Hi Feriel! Ready for our Python and Spanish session today?"},
            {"sender": "Feriel", "text": "Hello Maria! Yes, absolutely. Let's start with Python basics."}
        ],
        "Ahmed": [
            {"sender": "Ahmed", "text": "Hi! Let me know when you want to review the data science module."}
        ]
    }

if "shared_files" not in st.session_state:
    st.session_state.shared_files = {
        "Maria": [{"filename": "python_basics_cheat_sheet.pdf", "uploader": "Feriel", "size": "240 KB"}],
        "Ahmed": []
    }

if "visual_gallery" not in st.session_state:
    st.session_state.visual_gallery = {
        "Maria": [{"title": "UI Wireframe Sketch", "author": "Feriel", "type": "Design Layout"}],
        "Ahmed": []
    }

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

# --- MINIMALIST & CLEAN CSS STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #F3F3F4;
    }
    h1, h2, h3, h4 {
        color: #1B1F3B !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-weight: 600;
    }
    p, label, span {
        color: #1B1F3B;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .stButton>button {
        background-color: #3F72AF;
        color: white;
        border-radius: 6px;
        padding: 0.45rem 1.2rem;
        font-weight: 500;
        border: none;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .stButton>button:hover {
        background-color: #1B1F3B;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: APP LOGO & PROFILE CONFIGURATION ---
st.sidebar.markdown("# 🤝 PeerHub")
st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 User Profile Setup")
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

# --- NAVIGATION VIA SIDEBAR RADIO ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧭 Platform Navigation")
page = st.sidebar.radio(
    "Go to page:",
    [
        "🏠 Home & Overview", 
        "🔍 Smart Matching Engine", 
        "💰 Hour Bank & Credits", 
        "💬 Partner Chat & Direct Hub", 
        "🛡️ AI Excuse & Partner Audit"
    ]
)

# --- PAGE 1: HOME & OVERVIEW ---
if page == "🏠 Home & Overview":
    st.markdown("<h1 style='text-align: center; color: #1B1F3B;'>Welcome to PeerHub 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #3F72AF;'>Interactive Skill Exchange & Live Peer-to-Peer Learning Ecosystem</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    col_h1, col_h2, col_h3 = st.columns(3)
    with col_h1:
        st.markdown("### 🔍 Skill Barter")
        st.write("Match directly with peers based on what you can teach and what you want to learn using our live Supabase database.")
    with col_h2:
        st.markdown("### 💬 Direct P2P Hub")
        st.write("Communicate in real-time, upload study materials to the Document Vault, and archive visual sketches.")
    with col_h3:
        st.markdown("### 🛡️ Fair Governance")
        st.write("AI-powered excuse validation combined with partner sign-off quotas to protect community reliability.")
    
    st.markdown("---")
    st.info(f"👋 Hello **{user_name}**! Use the sidebar navigation above to explore the platform pages. **{db_status}**")

# --- PAGE 2: SMART MATCHING ENGINE ---
elif page == "🔍 Smart Matching Engine":
    st.header("🔍 Smart Skill Barter Matching Dashboard")
    st.write(f"Welcome back, **{user_name}**! {db_status}")
    st.write("Browse active community learners matching your teach & learn preferences:")
    
    if st.button("🔍 Find Perfect Match from Database"):
        with st.spinner("Searching live database for potential partners..."):
            try:
                response = supabase.table("Profiles").select("*").execute()
                users = response.data
                
                if not users:
                    users = [
                        {"name": "Maria", "teach_skill": "Spanish", "learn_skill": "Python Programming", "badge": "Committed Beginner 📌", "credits": 3},
                        {"name": "Ahmed", "teach_skill": "Python Programming", "learn_skill": "Spanish", "badge": "Reliable Partner ⭐", "credits": 5},
                        {"name": "Amir", "teach_skill": "UI/UX Design (Canva)", "learn_skill": "Python Programming", "badge": "Creative Contributor 🎨", "credits": 4}
                    ]
                
                matches = [u for u in users if u.get("name", "").lower() != user_name.lower()]
                
                if matches:
                    st.success(f"Found {len(matches)} active peer(s) in the live community!")
                    for m in matches:
                        with st.container():
                            st.markdown(f"""
                            ---
                            - 👤 **Peer Name:** {m.get('name')}
                            - 🎓 **Can Teach You:** `{m.get('teach_skill')}`
                            - 📚 **Wants to Learn:** `{m.get('learn_skill')}`
                            - 🏆 **Badge & Rating:** `{m.get('badge', 'Reliable Partner ⭐')}`
                            """)
                            if st.button(f"Connect & Propose Session with {m.get('name')}", key=f"req_{m.get('name')}"):
                                st.balloons()
                                st.info(f"🤝 Session proposal successfully sent to **{m.get('name')}**!")
                else:
                    st.info("No peers found in the database yet. Save your profile to join the queue!")
            except Exception as e:
                st.error(f"Could not fetch matches from database: {e}")

# --- PAGE 3: HOUR BANK & CREDITS ---
elif page == "💰 Hour Bank & Credits":
    st.header("💰 Hour Bank & Skill Credits")
    st.write(f"Track your earned hours and exchange value transparently within PeerHub, **{user_name}**.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Available Learning Credits", f"{st.session_state.user_credits} Hours", "+1 this week")
    col2.metric("Completed Sessions", f"{st.session_state.completed_sessions} Sessions", "100% Success")
    col3.metric("Net Credit Balance", f"{st.session_state.user_credits} hr Available", "🟢 Active Status")
    
    st.markdown("---")
    st.subheader("Session Verification & Credit Claim")
    completed_with = st.text_input("Completed session with partner name:", "Maria")
    session_topic = st.text_input("Session topic taught/learned:", "Python Basics & Grammar")
    
    if st.button("Claim +1 Hour Credit"):
        if completed_with:
            st.session_state.user_credits += 1
            st.session_state.completed_sessions += 1
            st.success(f"✅ Verified! 1 Hour credit successfully added to your account for the session with **{completed_with}**. New Balance: **{st.session_state.user_credits} Hours**.")
            st.balloons()
        else:
            st.warning("Please enter your partner's name first.")

# --- PAGE 4: PARTNER CHAT & DIRECT HUB ---
elif page == "💬 Partner Chat & Direct Hub":
    st.header("💬 Partner Chat & Direct Messaging Hub")
    st.write("Communicate directly with your assigned learning partners, share resources, and track session schedules.")
    
    chat_partner = st.selectbox("Select Active Chat Partner:", ["Maria", "Ahmed", "Amir", "Lina", "Chaima"], key="chat_partner_select")
    
    st.markdown(f"""
    <div style='background-color: #E2E8F0; border-left: 5px solid #3F72AF; padding: 14px; border-radius: 8px; margin-bottom: 15px;'>
        <h4 style='color: #1B1F3B !important; margin-bottom: 5px;'>📅 Upcoming Session Schedule</h4>
        <p style='color: #1B1F3B; margin: 2px 0;'><b>Partner:</b> {chat_partner} | <b>Agreed Time:</b> Tomorrow, 16:00 Algiers Time</p>
        <p style='color: #1B1F3B; margin: 2px 0;'><b>Topic:</b> Python Functions & Spanish Intermediate Conversation</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"🟢 **Connection State:** Connected securely with **{chat_partner}** (Active P2P Encrypted Channel)")
    st.markdown("---")
    
    if chat_partner not in st.session_state.chat_messages:
        st.session_state.chat_messages[chat_partner] = [
            {"sender": chat_partner, "text": f"Hello {user_name}! Looking forward to our next skill exchange session."}
        ]
    if chat_partner not in st.session_state.shared_files:
        st.session_state.shared_files[chat_partner] = []
    if chat_partner not in st.session_state.visual_gallery:
        st.session_state.visual_gallery[chat_partner] = []

    chat_col, vault_col = st.columns([2, 1])
    
    with chat_col:
        st.markdown(f"#### Conversation Thread with {chat_partner}")
        chat_container = st.container(height=350)
        with chat_container:
            for msg in st.session_state.chat_messages[chat_partner]:
                sender = msg.get("sender")
                text = msg.get("text")
                if sender == user_name:
                    st.markdown(f"<div style='text-align: right; background-color: #DBE2EF; padding: 10px; border-radius: 8px; margin: 6px 0;'><b>You:</b> {text}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='text-align: left; background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 10px; border-radius: 8px; margin: 6px 0;'><b>{sender}:</b> {text}</div>", unsafe_allow_html=True)
                    
        with st.form(key="chat_form", clear_on_submit=True):
            new_message = st.text_input("Type your message here:", placeholder="Type a message to coordinate your session...")
            submit_chat = st.form_submit_button("Send Message 📤")
            
            if submit_chat and new_message:
                st.session_state.chat_messages[chat_partner].append({"sender": user_name, "text": new_message})
                st.session_state.chat_messages[chat_partner].append({"sender": chat_partner, "text": f"Got it, {user_name}! Let's confirm."})
                st.rerun()

    with vault_col:
        st.markdown("#### 📁 Document Vault & Files")
        uploaded_file = st.file_uploader("Upload study material", type=["pdf", "png", "jpg", "py", "txt"])
        if uploaded_file:
            file_info = {"filename": uploaded_file.name, "uploader": user_name, "size": f"{uploaded_file.size // 1024} KB"}
            if file_info not in st.session_state.shared_files[chat_partner]:
                st.session_state.shared_files[chat_partner].append(file_info)
                st.success(f"Uploaded {uploaded_file.name} successfully!")
        
        if st.session_state.shared_files[chat_partner]:
            for f in st.session_state.shared_files[chat_partner]:
                st.markdown(f"""
                <div style='background-color: #FFFFFF; border: 1px solid #E2E8F0; padding: 10px; border-radius: 6px; margin-bottom: 8px;'>
                    📄 <b>{f.get('filename')}</b><br>
                    <small style='color: #64748B;'>Uploader: {f.get('uploader')} ({f.get('size')})</small><br>
                    📥 <a href='#' target='_blank' style='color: #3F72AF; text-decoration: none;'>Download Resource</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No files shared yet.")

        st.markdown("---")
        st.markdown("#### 🖼️ Session Visual Gallery")
        sketch_title = st.text_input("Visual Title / Sketch Name:", placeholder="e.g., Architecture Diagram")
        if st.button("Archive Visual Sketch"):
            if sketch_title:
                st.session_state.visual_gallery[chat_partner].append({"title": sketch_title, "author": user_name, "type": "Design Canvas"})
                st.success("Visual archived to gallery!")
        
        if st.session_state.visual_gallery[chat_partner]:
            for vis in st.session_state.visual_gallery[chat_partner]:
                st.markdown(f"""
                <div style='background-color: #FFFFFF; border: 1px solid #CBD5E1; padding: 10px; border-radius: 6px; margin-bottom: 8px;'>
                    🎨 <b>{vis.get('title')}</b><br>
                    <small style='color: #64748B;'>Archived by: {vis.get('author')}</small>
                </div>
                """, unsafe_allow_html=True)

# --- PAGE 5: AI EXCUSE & PARTNER AUDIT ---
elif page == "🛡️ AI Excuse & Partner Audit":
    st.header("🛡️ Partner Verification & AI Excuse Audit System")
    st.write("Need to reschedule a session? Submit your excuse for dual-layer verification: **Partner Sign-off** & **AI Policy Check**.")
    
    current_used = st.session_state.excuse_count
    remaining = max(0, 2 - current_used)
    st.info(f"📅 **User Monthly Policy Tracker:** You have used **{current_used} of 2** allowed approved excuses this month. (**{remaining}** remaining)")
    
    st.markdown("### 🎬 Demo Simulation Mode")
    sim_mode = st.radio(
        "Switch View Mode for Demo Recording:",
        ["1. User View: Submit Excuse & Request Rescheduling", "2. Partner View: Review & Write Custom Note"],
        horizontal=True
    )
    
    col_a, col_b = st.columns(2)
    with col_a:
        assigned_partner = st.selectbox("Select Your Learning Partner:", ["Maria", "Ahmed", "Amir", "Lina", "Chaima"], key="audit_partner_select")
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
        
        p_approvals_used = st.session_state.partner_approval_count
        st.info(f"🛡️ **Partner Governance Quota:** Partner Approvals Used: **{p_approvals_used} of 5** allowed this month.")
        
        current_pending = st.session_state.get("pending_excuse", {})
        p_user = current_pending.get("user", user_name)
        p_text = current_pending.get("text", "No excuse text provided.")
        p_category = current_pending.get("excuse_type", excuse_type_label)
        
        st.write(f"👤 **Reviewing excuse from {p_user}:** '{p_text}' (Category: *{p_category}*)")
        
        st.markdown(
            "> ⚖️ **PeerHub Rights Protection Disclaimer:** PeerHub protects your learning rights, giving you the power to carefully review, comment, and explicitly accept or reject your partner's excuse."
        )
        
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
    
    st.table(st.session_state.audit_log)

st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748B;'>PeerHub Full-Stack App — Powered by Supabase & Streamlit (Thirduni - October 2026)</p>", unsafe_allow_html=True)
