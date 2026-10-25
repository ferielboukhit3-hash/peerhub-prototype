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
            "author": "malak dechicha",
            "time": "Yesterday",
            "content": "Working on advanced Spanish verb conjugations today. If anyone wants to practice conversational tandem sessions this evening, let me know!",
            "likes": 8,
            "comments": 1,
            "liked_by_user": True
        },
        {
            "id": 3,
            "author": "Karima khelifi",
            "time": "3 days ago",
            "content": "Shared a new template for digital marketing analytics and ROI tracking in the Document Vault. Check it out if you're exploring e-commerce metrics!",
            "likes": 19,
            "comments": 5,
            "liked_by_user": False
        }
    ]

    # Community Directory Users (Mock + Supabase Ready)
    st.session_state.directory_users = [
        {"name": "Feriel Boukhit", "age": 21, "gender": "Woman", "teach": "Python Programming (Intermediate)", "learn": "Spanish (Beginner)", "avatar": "👩‍💻", "rating": 4.9},
        {"name": "malak dechicha", "age": 22, "gender": "Woman", "teach": "Spanish & Literature (Advanced)", "learn": "Python Programming", "avatar": "📚", "rating": 4.8},
        {"name": "lina Larbi", "age": 24, "gender": "Man", "teach": "Data Structures & Algorithms", "learn": "Digital Marketing", "avatar": "👨‍💻", "rating": 4.7},
        {"name": "Sarah lily", "age": 23, "gender": "Woman", "teach": "UI/UX Design & Figma", "learn": "French Fluency", "avatar": "🎨", "rating": 5.0},
        {"name": "Yacine toumi", "age": 25, "gender": "Man", "teach": "Macroeconomics & Finance", "learn": "Korean Language", "avatar": "📊", "rating": 4.6}
    ]

    # Chat Conversations
    st.session_state.chats = {
        "malak dechicha": [
            {"sender": "malak dechicha", "text": "Hi Feriel! Are we still on for our Spanish & Python exchange at 4 PM?", "time": "3:15 PM"},
            {"sender": "Feriel", "text": "Yes absolutely! I have my Jupyter notebook ready for the Python algorithms part.", "time": "3:20 PM"}
        ],
        "Sarah Chen": [
            {"sender": "Sarah lily", "text": "Check out the wireframes I uploaded to the shared canvas.", "time": "Yesterday"},
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
    
    # Create New Post Box
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

    # Display Feed Posts
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

    # Search and Filters
    col_search, col_gender, col_skill = st.columns([2, 1, 1])
    with col_search:
        search_query = st.text_input("🔍 Search users by name or skill", placeholder="Type a name or topic...")
    with col_gender:
        gender_filter = st.selectbox("Filter by Gender", ["All", "Woman", "Man"])
    with col_skill:
        skill_filter = st.selectbox("Filter by Skill Domain", ["All", "Python Programming", "Spanish", "Digital Marketing", "UI/UX Design", "Macroeconomics"])

    st.markdown("---")

    # Filter Logic
    filtered_users = st.session_state.directory_users
    if search_query:
        filtered_users = [u for u in filtered_users if search_query.lower() in u['name'].lower() or search_query.lower() in u['teach'].lower() or search_query.lower() in u['learn'].lower()]
    if gender_filter != "All":
        filtered_users = [u for u in filtered_users if u['gender'] == gender_filter]
    if skill_filter != "All":
        filtered_users = [u for u in filtered_users if skill_filter.lower() in u['teach'].lower() or skill_filter.lower() in u['learn'].lower()]

    # Render User Cards in Grid
    if not filtered_users:
        st.warning("No matching users found. Try broadening your search criteria.")
    else:
        cols = st.columns(2)
        for i, user in enumerate(filtered_users):
            with cols[i % 2]:
                st.markdown(f"""
                    <div class="card">
                        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                            <div style="font-size: 2.5rem; background: #E6F0FA; padding: 0.5rem; border-radius: 50%; width: 64px; height: 64px; display: flex; align-items: center; justify-content: center;">
                                {user['avatar']}
                            </div>
                            <div>
                                <h3 style="margin: 0; font-size: 1.2rem;">{user['name']}</h3>
                                <p style="margin: 0; color: #6E7191; font-size: 0.9rem;">{user['gender']} · {user['age']} yrs old · ⭐ {user['rating']}</p>
                            </div>
                        </div>
                        <p style="margin: 0.2rem 0;"><strong>🎓 Can Teach:</strong> {user['teach']}</p>
                        <p style="margin: 0.2rem 0 1rem 0;"><strong>📚 Wants to Learn:</strong> {user['learn']}</p>
                    </div>
                """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. CHATS & DIRECT MESSAGING HUB (AI-CHAT STYLE)
# -----------------------------------------------------------------------------
elif page == "💬 Chats & Direct Hub":
    st.markdown("# 💬 Partner Chat & Direct Messaging Hub")
    st.markdown("Modern AI-assisted chat interface for seamless skill exchange and resource sharing.")

    # Dual-pane layout: Chat on left, Shared Resources on right
    chat_col, res_col = st.columns([3, 2])

    with chat_col:
        st.markdown("### Active Conversation")
        selected_partner = st.selectbox("Select Learning Partner", list(st.session_state.chats.keys()))
        
        # Chat container box
        chat_box = st.container()
        with chat_box:
            st.markdown('<div class="card" style="height: 380px; overflow-y: auto;">', unsafe_allow_html=True)
            for msg in st.session_state.chats[selected_partner]:
                alignment = "text-align: right;" if msg["sender"] == "Feriel" else "text-align: left;"
                bg_color = "#E6F0FA" if msg["sender"] == "Feriel" else "#FFFFFF"
                border_col = "#0A66C2" if msg["sender"] == "Feriel" else "#E1E1E6"
                st.markdown(f"""
                    <div style="{alignment} margin-bottom: 0.8rem;">
                        <span style="font-size: 0.75rem; color: #6E7191;">{msg['sender']} · {msg['time']}</span>
                        <div style="background-color: {bg_color}; border: 1px solid {border_col}; padding: 0.6rem 1rem; border-radius: 8px; display: inline-block; max-width: 80%; text-align: left;">
                            {msg['text']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Interactive Chat Input Area with Media/File Uploader, Gallery & Voice Choice
        with st.form("chat_input_form", clear_on_submit=True):
            user_message = st.text_input("Message your partner...", placeholder="Type message or prompt AI assistant...")
            
            c_input1, c_input2, c_input3, c_input4 = st.columns([1, 1, 1, 2])
            with c_input1:
                attach_doc = st.form_submit_button("📎 Document Vault")
            with c_input2:
                attach_img = st.form_submit_button("🖼️ Visual Gallery")
            with c_input3:
                voice_msg = st.form_submit_button("🎤 Voice Note")
            with c_input4:
                send_msg = st.form_submit_button("Send Message 🚀", use_container_width=True)

            if send_msg and user_message.strip():
                st.session_state.chats[selected_partner].append({
                    "sender": "Feriel",
                    "text": user_message.strip(),
                    "time": datetime.datetime.now().strftime("%I:%M %p")
                })
                st.rerun()
            elif attach_doc:
                st.toast("Document Vault attached to chat session.")
            elif attach_img:
                st.toast("Visual Gallery attached to chat session.")
            elif voice_msg:
                st.toast("Simulated Voice Message recorded and sent.")

    with res_col:
        st.markdown("### 🗂️ Shared Resources & Sketches")
        st.markdown("""
            <div class="card">
                <h4>📌 Pinned Canvas Items</h4>
                <p style="font-size: 0.9rem; color: #6E7191;">Collaborative artifacts shared during sessions with <strong>%s</strong>:</p>
                <ul>
                    <li><strong>Python_Trade_Tariff_Parser.py</strong> (Script)</li>
                    <li><strong>Spanish_Verbs_CheatSheet.pdf</strong> (Document)</li>
                    <li><strong>UI_Wireframe_Sketch_v2.png</strong> (Design)</li>
                </ul>
                <hr style="border: 0; border-top: 1px solid #E1E1E6; margin: 1rem 0;">
                <h4>🤖 AI Session Summary</h4>
                <p style="font-size: 0.9rem;">Both participants successfully reviewed data parsing structures and practiced 15 minutes of conversational Spanish.</p>
            </div>
        """ % selected_partner, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. MY PROFILE PAGE (STANDARD & STRUCTURED)
# -----------------------------------------------------------------------------
elif page == "👤 My Profile":
    # Top Header Status / Utility Bar
    top_col1, top_col2, top_col3 = st.columns([3, 1, 1])
    with top_col1:
        st.markdown("# 👤 My Professional Portfolio")
    with top_col2:
        st.markdown("🕒 **Schedule:** Active")
    with top_col3:
        dark_mode_toggle = st.toggle("Dark/Light Mode", value=st.session_state.profile['dark_mode'])
        if dark_mode_toggle != st.session_state.profile['dark_mode']:
            st.session_state.profile['dark_mode'] = dark_mode_toggle
            st.toast("Theme preference updated!")

    # Custom Cover Banner & Profile Avatar Header
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0A66C2 0%, #1B1F3B 100%); height: 140px; border-radius: 12px; margin-bottom: -50px;"></div>
        <div style="display: flex; align-items: flex-end; gap: 1.5rem; padding: 0 2rem; margin-bottom: 1.5rem;">
            <div style="font-size: 4rem; background: #FFFFFF; border: 4px solid #FFFFFF; border-radius: 50%; width: 90px; height: 90px; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                👩‍💻
            </div>
            <div style="padding-top: 1.5rem;">
                <h2 style="margin: 0; color: #1B1F3B;">%s</h2>
                <p style="margin: 0; color: #6E7191; font-weight: 500;">%s · 📍 %s</p>
            </div>
        </div>
    """ % (st.session_state.profile['full_name'], st.session_state.profile['title'], st.session_state.profile['location']), unsafe_allow_html=True)

    # Analytics Metrics Row
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
            <div class="card" style="text-align: center;">
                <h4 style="margin:0; color: #6E7191;">Completed Sessions</h4>
                <h2 style="margin:0; color: #0A66C2; font-size: 2rem;">{st.session_state.profile['completed_sessions']}</h2>
                <span style="font-size: 0.8rem; color: #28a745;">↑ 100% Success</span>
            </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
            <div class="card" style="text-align: center;">
                <h4 style="margin:0; color: #6E7191;">Hours Earned</h4>
                <h2 style="margin:0; color: #0A66C2; font-size: 2rem;">{st.session_state.profile['hours_earned']} hrs</h2>
                <span style="font-size: 0.8rem; color: #28a745;">+1 this week</span>
            </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
            <div class="card" style="text-align: center;">
                <h4 style="margin:0; color: #6E7191;">Community Rating</h4>
                <h2 style="margin:0; color: #0A66C2; font-size: 2rem;">{st.session_state.profile['rating']} / 5.0</h2>
                <span style="font-size: 0.8rem; color: #f39c12;">⭐ Top Rated</span>
            </div>
        """, unsafe_allow_html=True)

    # Editable Bio ("About Me") Section
    st.markdown("### 📝 About Me")
    with st.form("profile_edit_form"):
        edited_about = st.text_area("Edit your professional summary:", value=st.session_state.profile['about'], height=100)
        
        st.markdown("### 💡 Skills & Expertise & Proficiency Levels")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            teach_skill_input = st.text_input("Skill to Teach", value=st.session_state.profile['teach_skill'])
            teach_level_input = st.selectbox("Primary Teaching Skill Level", ["Beginner", "Intermediate", "Advanced", "Expert"], index=1)
        with col_s2:
            learn_skill_input = st.text_input("Skill to Learn", value=st.session_state.profile['learn_skill'])
            learn_level_input = st.selectbox("Primary Learning Goal Level", ["Beginner", "Intermediate", "Advanced"], index=0)

        st.markdown("### 🔗 Professional Links & Portfolio")
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            linkedin_input = st.text_input("LinkedIn Profile URL", value=st.session_state.profile['linkedin'])
        with col_l2:
            github_input = st.text_input("GitHub Profile URL", value=st.session_state.profile['github'])

        save_profile_btn = st.form_submit_button("💾 Save Profile Updates to Supabase")

        if save_profile_btn:
            st.session_state.profile['about'] = edited_about
            st.session_state.profile['teach_skill'] = teach_skill_input
            st.session_state.profile['teach_level'] = teach_level_input
            st.session_state.profile['learn_skill'] = learn_skill_input
            st.session_state.profile['learn_level'] = learn_level_input
            st.session_state.profile['linkedin'] = linkedin_input
            st.session_state.profile['github'] = github_input
            st.success("Profile successfully updated and synced with Supabase Profiles table!")

    # Badges & Streaks Showcase
    st.markdown("### 🏆 Honors & Badges")
    st.markdown("""
        <div>
            <span class="badge">Reliable Partner ⭐ (Exceptional Attendance)</span>
            <span class="badge">Streak Master 🔥 (4 Weeks Active)</span>
            <span class="badge">Python Pro 🐍 (Collaborative Coding)</span>
        </div>
    """, unsafe_allow_html=True)

    # User's Own Posts Section
    st.markdown("### 📌 My Shared Posts")
    user_posts = [p for p in st.session_state.posts if p['author'] == st.session_state.profile['full_name']]
    if not user_posts:
        st.info("You haven't published any posts yet. Head over to the Community Feed to share your first update!")
    else:
        for p in user_posts:
            st.markdown(f"""
                <div class="card">
                    <span style="color: #6E7191; font-size: 0.85rem;">{p['time']}</span>
                    <p style="margin-top: 0.5rem; font-size: 1rem;">{p['content']}</p>
                    <span style="font-size: 0.85rem; color: #0A66C2;">❤️ {p['likes']} Likes · 💬 {p['comments']} Comments</span>
                </div>
            """, unsafe_allow_html=True)
