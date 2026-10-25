import streamlit as st
import datetime

# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & THEMING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="PeerHub — Interactive Skill Exchange",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom minimalist styling (Platinum background #F3F3F4, Space Indigo #1B1F3B, Clean Blue #0A66C2)
st.markdown("""
    <style>
        .stApp {
            background-color: #F3F3F4;
            color: #1B1F3B;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #1B1F3B !important;
            font-weight: 700;
        }
        .stButton>button {
            background-color: #0A66C2;
            color: white;
            border-radius: 6px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: background-color 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #084e96;
            color: white;
        }
        .card {
            background-color: #FFFFFF;
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid #E1E1E6;
            box-shadow: 0 2px 4px rgba(27, 31, 59, 0.04);
            margin-bottom: 1rem;
        }
        .badge {
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 600;
            background-color: #E6F0FA;
            color: #0A66C2;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }
        .sidebar .stRadio label {
            color: #1B1F3B;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    
    # User Profile State
    st.session_state.profile = {
        "name": "Feriel",
        "full_name": "Feriel Boukhit",
        "title": "International Trade Student & Aspiring Full-Stack Developer",
        "location": "Algiers, Algeria",
        "about": "Third-year university student studying Commercial Sciences & International Trade at University of Algiers 3. Passionate about Python, languages, digital marketing, and international economic diplomacy.",
        "teach_skill": "Python Programming",
        "teach_level": "Intermediate",
        "learn_skill": "Spanish",
        "learn_level": "Beginner",
        "linkedin": "linkedin.com/in/feriel-boukhit",
        "github": "github.com/ferielboukhit3-hash",
        "gender": "Woman",
        "age": 21,
        "completed_sessions": 4,
        "hours_earned": 5,
        "rating": 4.9,
        "dark_mode": False
    }

    # Community Posts Feed
    st.session_state.posts = [
        {
            "id": 1,
            "author": "Feriel Boukhit",
            "time": "2 hours ago",
            "content": "Just finished building my first collaborative Python script for tracking international trade tariffs! Excited to exchange ideas with fellow peers on PeerHub 🚀",
            "likes": 12,
            "comments": 3,
            "liked_by_user": False
        },
        {
            "id": 2,
            "author": "Anfal Fittih",
            "time": "Yesterday",
            "content": "Working on advanced Spanish verb conjugations today. If anyone wants to practice conversational tandem sessions this evening, let me know!",
            "likes": 8,
            "comments": 1,
            "liked_by_user": True
        },
        {
            "id": 3,
            "author": "Karim Benzema",
            "time": "3 days ago",
            "content": "Shared a new template for digital marketing analytics and ROI tracking in the Document Vault. Check it out if you're exploring e-commerce metrics!",
            "likes": 19,
            "comments": 5,
            "liked_by_user": False
        }
    ]

    # Community Directory Users
    st.session_state.directory_users = [
        {"name": "Feriel Boukhit", "age": 21, "gender": "Woman", "teach": "Python Programming (Intermediate)", "learn": "Spanish (Beginner)", "avatar": "👩‍💻", "rating": 4.9},
        {"name": "Anfal Fittih", "age": 22, "gender": "Woman", "teach": "Spanish & Literature (Advanced)", "learn": "Python Programming", "avatar": "📚", "rating": 4.8},
        {"name": "Mehdi Larbi", "age": 24, "gender": "Man", "teach": "Data Structures & Algorithms", "learn": "Digital Marketing", "avatar": "👨‍💻", "rating": 4.7},
        {"name": "Sarah Chen", "age": 23, "gender": "Woman", "teach": "UI/UX Design & Figma", "learn": "French Fluency", "avatar": "🎨", "rating": 5.0},
        {"name": "Yacine Brahimi", "age": 25, "gender": "Man", "teach": "Macroeconomics & Finance", "learn": "Korean Language", "avatar": "📊", "rating": 4.6}
    ]

    # Chat Conversations
    st.session_state.chats = {
        "Anfal Fittih": [
            {"sender": "Anfal Fittih", "text": "Hi Feriel! Are we still on for our Spanish & Python exchange at 4 PM?", "time": "3:15 PM"},
            {"sender": "Feriel", "text": "Yes absolutely! I have my Jupyter notebook ready for the Python algorithms part.", "time": "3:20 PM"}
        ],
        "Sarah Chen": [
            {"sender": "Sarah Chen", "text": "Check out the wireframes I uploaded to the shared canvas.", "time": "Yesterday"},
            {"sender": "Feriel", "text": "Looks super clean and minimalist! Love the color scheme.", "time": "Yesterday"}
        ]
    }

# -----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.markdown("## 🤝 PeerHub")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "🧭 Platform Navigation",
    [
        "🏠 Home & Posts (Community Feed)",
        "👥 Community Directory",
        "💬 Chats & Direct Hub",
        "👤 My Profile"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Session Status")
st.sidebar.info(f"**Active User:** {st.session_state.profile['name']}\n\n**Credits:** {st.session_state.profile['hours_earned']} hrs earned")

# -----------------------------------------------------------------------------
# 1. HOME & POSTS PAGE (COMMUNITY FEED)
# -----------------------------------------------------------------------------
if page == "🏠 Home & Posts (Community Feed)":
    st.markdown("# 🏠 Community Feed & Learning Wall")
    st.markdown("Share your learning progress, discover insights from peers, and collaborate in real-time.")
    
    with st.form("new_post_form", clear_on_submit=True):
        st.markdown("### ✍️ Share an update or question")
        new_post_content = st.text_area("What are you working on today?", placeholder="Write your thoughts, ask a question, or share a milestone...", height=100)
        col1, col2 = st.columns([6, 1])
        with col2:
            submitted = st.form_submit_button("Post Update")
        
        if submitted and new_post_content.strip():
            new_entry = {
                "id": len(st.session_state.posts) + 1,
                "author": st.session_state.profile['full_name'],
                "time": "Just now",
                "content": new_post_content.strip(),
                "likes": 0,
                "comments": 0,
                "liked_by_user": False
            }
            st.session_state.posts.insert(0, new_entry)
            st.success("Post published successfully!")
            st.rerun()

    st.markdown("---")
    st.markdown("### 📰 Recent Community Activity")

    for idx, post in enumerate(st.session_state.posts):
        with st.container():
            st.markdown(f"""
                <div class="card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <strong>👤 {post['author']}</strong>
                        <span style="color: #6E7191; font-size: 0.85rem;">{post['time']}</span>
                    </div>
                    <p style="font-size: 1.05rem; color: #1B1F3B; margin-bottom: 1rem;">{post['content']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns([1, 1, 4])
            with c1:
                like_label = f"❤️ {post['likes']}" if not post['liked_by_user'] else f"💖 {post['likes']}"
                if st.button(like_label, key=f"like_{post['id']}"):
                    if post['liked_by_user']:
                        post['likes'] -= 1
                        post['liked_by_user'] = False
                    else:
                        post['likes'] += 1
                        post['liked_by_user'] = True
                    st.rerun()
            with c2:
                if st.button(f"💬 {post['comments']} Comments", key=f"comment_{post['id']}"):
                    st.toast(f"Opening discussion thread for post #{post['id']}")

# -----------------------------------------------------------------------------
# 2. COMMUNITY DIRECTORY PAGE
# -----------------------------------------------------------------------------
elif page == "👥 Community Directory":
    st.markdown("# 👥 Community Directory")
    st.markdown("Explore active learners and instructors across the PeerHub network.")

    col_search, col_gender, col_skill = st.columns([2, 1, 1])
    with col_search:
        search_query = st.text_input("🔍 Search users by name or skill", placeholder="Type a name or topic...")
    with col_gender:
        gender_filter = st.selectbox("Filter by Gender", ["All", "Woman", "Man"])
    with col_skill:
        skill_filter = st.selectbox("Filter by Skill Domain", ["All", "Python Programming", "Spanish", "Digital Marketing", "UI/UX Design", "Macroeconomics"])

    st.markdown("---")

    filtered_users = st.session_state.directory_users
    if search_query:
        filtered_users = [u for u in filtered_users if search_query.lower() in u['name'].lower() or search_query.lower() in u['teach'].lower() or search_query.lower() in u['learn'].lower()]
    if gender_filter != "All":
        filtered_users = [u for u in filtered_users if u['gender'] == gender_filter]
    if skill_filter != "All":
        filtered_users = [u for u in filtered_users if skill_filter.lower() in u['teach'].lower() or skill_filter.lower() in u['learn'].lower()]

    if not filtered_users:
        st.warning("No matching users found. Try broadening your search criteria.")
    else:
        for u in filtered_users:
            card_html = (
                f"<div class='card'>"
                f"<h3>{u['avatar']} {u['name']} ({u['gender']}, {u['age']})</h3>"
                f"<p><b>Can Teach:</b> {u['teach']}</p>"
                f"<p><b>Wants to Learn:</b> {u['learn']}</p>"
                f"<p><b>Community Rating:</b> ⭐ {u['rating']} / 5.0</p>"
                f"</div>"
            )
            st.markdown(card_html, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. CHATS & DIRECT HUB
# -----------------------------------------------------------------------------
elif page == "💬 Chats & Direct Hub":
    st.markdown("# 💬 Chats & Direct Messaging Hub")
    st.markdown("Coordinate sessions with learning partners, share resources, and upload files.")

    chat_partner = st.selectbox("Select Partner Conversation:", list(st.session_state.chats.keys()))
    
    chat_col, vault_col = st.columns([2, 1])
    with chat_col:
        st.markdown(f"### 💬 Conversation with {chat_partner}")
        chat_box = st.container(height=350)
        with chat_box:
            for msg in st.session_state.chats[chat_partner]:
                sender = msg['sender']
                text = msg['text']
                time = msg.get('time', '')
                if sender == "Feriel":
                    st.markdown(f"<div style='text-align: right; background-color: #DBE2EF; padding: 10px; border-radius: 8px; margin: 6px 0;'><b>You:</b> {text} <br><small style='color: #6E7191;'>{time}</small></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='text-align: left; background-color: #FFFFFF; border: 1px solid #E1E1E6; padding: 10px; border-radius: 8px; margin: 6px 0;'><b>{sender}:</b> {text} <br><small style='color: #6E7191;'>{time}</small></div>", unsafe_allow_html=True)

        with st.form("chat_input_form", clear_on_submit=True):
            user_msg = st.text_input("Type your message...", placeholder="Coordinate your study session...")
            c_btn1, c_btn2, c_btn3 = st.columns([4, 1, 1])
            with c_btn1:
                send_clicked = st.form_submit_button("Send 📤")
            with c_btn2:
                attachment_btn = st.form_submit_button("📎 File")
            with c_btn3:
                mic_btn = st.form_submit_button("🎤 Voice")
                
            if send_clicked and user_msg.strip():
                st.session_state.chats[chat_partner].append({"sender": "Feriel", "text": user_msg.strip(), "time": "Just now"})
                st.session_state.chats[chat_partner].append({"sender": chat_partner, "text": f"Got it, Feriel! Let's connect.", "time": "Just now"})
                st.rerun()
            elif attachment_btn:
                st.toast("📎 File vault picker opened.")
            elif mic_btn:
                st.toast("🎤 Voice message recorded successfully.")

    with vault_col:
        st.markdown("### 📁 Document Vault")
        uploaded_file = st.file_uploader("Upload study material", type=["pdf", "png", "jpg", "py", "txt"])
        if uploaded_file:
            st.success(f"Uploaded {uploaded_file.name} successfully!")
        st.info("Shared study resources and sketches appear here securely.")

# -----------------------------------------------------------------------------
# 4. MY PROFILE PAGE
# -----------------------------------------------------------------------------
elif page == "👤 My Profile":
    st.markdown("# 👤 My Professional Profile")
    
    # Top Utility Bar
    p_col1, p_col2, p_col3 = st.columns(3)
    with p_col1:
        if st.button("📅 Session Time Schedule"):
            st.info("🕒 Your upcoming sessions: Python & Spanish exchange tomorrow at 16:00.")
    with p_col2:
        if st.button("⚙️ Parameters & Settings"):
            st.session_state.profile['dark_mode'] = st.toggle("Dark Mode Toggle", value=st.session_state.profile['dark_mode'])
    with p_col3:
        st.markdown(f"**Status:** 🟢 Available for Sessions")

    st.markdown("---")

    # Profile Header Card with Banner & Avatar
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #0A66C2 0%, #1B1F3B 100%); height: 130px; border-radius: 12px 12px 0 0; padding: 20px; color: white;">
            <h2>💼 PeerHub Learning Portfolio</h2>
        </div>
        <div class="card" style="border-radius: 0 0 12px 12px; margin-top: -1rem;">
            <h2>👩‍💻 {st.session_state.profile['full_name']}</h2>
            <p style="color: #6E7191; font-size: 1.05rem;">{st.session_state.profile['title']}</p>
            <p style="color: #6E7191; font-size: 0.95rem;">📍 {st.session_state.profile['location']}</p>
        </div>
    """, unsafe_allow_html=True)

    profile_col1, profile_col2 = st.columns([2, 1])

    with profile_col1:
        st.markdown("### 📝 About Me")
        new_about = st.text_area("Edit your bio:", value=st.session_state.profile['about'], height=100)
        if new_about != st.session_state.profile['about']:
            st.session_state.profile['about'] = new_about

        st.markdown("### 💡 Skills & Proficiency Levels")
        s_col1, s_col2 = st.columns(2)
        with s_col1:
            st.session_state.profile['teach_skill'] = st.selectbox("Teaching Skill:", ["Python Programming", "Spanish", "French", "Digital Marketing"], index=0)
            st.session_state.profile['teach_level'] = st.selectbox("Teaching Level:", ["Beginner", "Intermediate", "Advanced", "Expert"], index=1)
        with s_col2:
            st.session_state.profile['learn_skill'] = st.selectbox("Learning Goal:", ["Spanish", "Python Programming", "Korean", "Data Science"], index=0)
            st.session_state.profile['learn_level'] = st.selectbox("Learning Level:", ["Beginner", "Intermediate", "Advanced"], index=0)

        st.markdown("### ✍️ My Published Posts")
        user_posts = [p for p in st.session_state.posts if p['author'] == st.session_state.profile['full_name']]
        if user_posts:
            for p in user_posts:
                st.markdown(f"<div class='card'>💬 <b>{p['time']}:</b> {p['content']}</div>", unsafe_allow_html=True)
        else:
            st.info("You haven't published any posts yet.")

    with profile_col2:
        st.markdown("### 📊 Performance Metrics")
        st.metric("Completed Sessions", f"{st.session_state.profile['completed_sessions']}", "+1 this week")
        st.metric("Hours Earned", f"{st.session_state.profile['hours_earned']} hrs", "🟢 Active Balance")
        st.metric("Community Rating", f"⭐ {st.session_state.profile['rating']} / 5.0", "Top Rated")

        st.markdown("### 🏆 Streaks & Badges")
        st.markdown("<span class='badge'>Reliable Partner ⭐</span>", unsafe_allow_html=True)
        st.markdown("<span class='badge'>Streak Master 🔥</span>", unsafe_allow_html=True)
        st.markdown("<span class='badge'>Python Pro 🐍</span>", unsafe_allow_html=True)
        st.markdown("<span class='badge'>Top Contributor 🚀</span>", unsafe_allow_html=True)
