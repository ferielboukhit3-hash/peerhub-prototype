import streamlit as st
from datetime import datetime, date, time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="PeerHub — Interactive Skill Exchange",
    page_icon="🤝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GLOBAL STYLING & COLOR PALETTE ---
# Platinum: #F3F3F4, Space Indigo: #1B1F3B, Clean Blue: #0A66C2
st.markdown("""
    <style>
        /* Main Theme Background */
        .stApp {
            background-color: #F3F3F4;
            color: #1B1F3B;
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E2E8F0;
        }
        
        /* Headers & Typography */
        h1, h2, h3, h4, h5, h6 {
            color: #1B1F3B !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* Custom Cards */
        .peer-card {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            margin-bottom: 16px;
            transition: transform 0.2s ease;
        }
        .peer-card:hover {
            border-color: #0A66C2;
            box-shadow: 0 4px 12px rgba(10, 102, 194, 0.08);
        }
        
        /* Primary Buttons */
        .stButton>button {
            background-color: #0A66C2;
            color: #FFFFFF;
            border-radius: 8px;
            border: none;
            font-weight: 600;
            padding: 0.5rem 1rem;
        }
        .stButton>button:hover {
            background-color: #084e96;
            color: #FFFFFF;
        }
        
        /* Status Badges */
        .badge-online { background-color: #DEF7EC; color: #03543F; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: 600; }
        .badge-session { background-color: #FEF08A; color: #713F12; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: 600; }
        .badge-away { background-color: #F3F4F6; color: #4B5563; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- SAFE SESSION STATE INITIALIZATION ---
def initialize_session_state():
    if 'profile' not in st.session_state:
        st.session_state.profile = {
            'full_name': 'Feriel Boukhit',
            'title': 'Full-Stack Developer & UI/UX Designer',
            'location': 'Algiers, Algeria',
            'bio': 'Passionate about building seamless digital experiences, modern web applications, and exploring collaborative peer-to-peer learning networks.',
            'skills': {'Python': 'Advanced', 'React / Next.js': 'Intermediate', 'UI/UX Design': 'Expert', 'Machine Learning': 'Intermediate'},
            'credits': 5,
            'completed_sessions': 14,
            'rating': 4.9,
            'badges': ['Reliable Partner ⭐', 'Streak Master 🔥', 'Python Pro 🐍', 'Design Guru 🎨'],
            'avatar': None
        }
    
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "🏠 Home & Posts"

    if 'posts' not in st.session_state:
        st.session_state.posts = [
            {
                'author': 'Alex Rivera',
                'role': 'Data Science Enthusiast',
                'time': '2 hours ago',
                'content': 'Just completed a 3-hour session on advanced Pandas data manipulation with Feriel! The credit exchange system is fantastic. 🚀',
                'likes': 12,
                'comments': ['Awesome work!', 'Would love to join the next session!']
            },
            {
                'author': 'Sarah Jenkins',
                'role': 'Product Designer',
                'time': '5 hours ago',
                'content': 'Looking for someone to practice conversational Spanish with in exchange for Figma & Design System mentorship. Drop a message!',
                'likes': 8,
                'comments': ['Sent you a DM!']
            }
        ]

    if 'peers' not in st.session_state:
        st.session_state.peers = [
            {'id': 'alex', 'name': 'Alex Rivera', 'title': 'Data Scientist', 'status': 'Online', 'skills': ['Python', 'SQL', 'Machine Learning'], 'rating': 4.8},
            {'id': 'sarah', 'name': 'Sarah Jenkins', 'title': 'UI/UX Designer', 'status': 'In a session', 'skills': ['Figma', 'Design Systems', 'User Research'], 'rating': 5.0},
            {'id': 'liam', 'name': 'Liam Chen', 'title': 'Full Stack Developer', 'status': 'Away', 'skills': ['JavaScript', 'Node.js', 'React'], 'rating': 4.7},
            {'id': 'elena', 'name': 'Elena Rostova', 'title': 'Mobile Developer', 'status': 'Online', 'skills': ['Flutter', 'Swift', 'Kotlin'], 'rating': 4.9}
        ]

    if 'viewing_profile' not in st.session_state:
        st.session_state.viewing_profile = None

    if 'chats' not in st.session_state:
        st.session_state.chats = {
            'Alex Rivera': [
                {'sender': 'Alex', 'text': 'Hey Feriel! Ready for our Python review session today?', 'time': '10:15 AM'},
                {'sender': 'Feriel', 'text': 'Hi Alex! Yes absolutely, let me pull up the shared resources notebook.', 'time': '10:18 AM'}
            ],
            'Sarah Jenkins': [
                {'sender': 'Sarah', 'text': 'Loved your design feedback on the new wireframes.', 'time': 'Yesterday'}
            ]
        }

    if 'scheduled_sessions' not in st.session_state:
        st.session_state.scheduled_sessions = [
            {'peer': 'Alex Rivera', 'topic': 'Python & Data Structures', 'date': str(date.today()), 'time': '14:00', 'status': 'Confirmed'}
        ]

initialize_session_state()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("## 🤝 PeerHub")
    st.markdown("### 🧭 Platform Navigation")
    
    nav_options = [
        "🏠 Home & Posts", 
        "👥 Peers Directory", 
        "💬 Chats & Direct Hub", 
        "📅 Course Schedule", 
        "👤 My Profile"
    ]
    
    # Determine default index
    current_selection = st.session_state.get('selected_page', "🏠 Home & Posts")
    if current_selection not in nav_options:
        current_selection = "🏠 Home & Posts"
        
    selected_nav = st.radio("Go to", nav_options, index=nav_options.index(current_selection), label_visibility="collapsed")
    st.session_state.selected_page = selected_nav

    st.markdown("---")
    st.markdown("### ⚡ Quick Session Status")
    st.info(f"**Active User:** {st.session_state.profile['full_name']}\n\n**Hour Bank:** {st.session_state.profile['credits']} hrs earned")

# ==========================================
# 1. HOME & POSTS PAGE (COMMUNITY FEED)
# ==========================================
if st.session_state.selected_page == "🏠 Home & Posts":
    st.title("🏠 Community Feed & Posts")
    st.markdown("Share your learning milestones, brainstorm ideas, or ask the community for assistance.")
    
    # Create new post box
    with st.form("new_post_form", clear_on_submit=True):
        st.markdown("### ✨ Create New Post")
        post_content = st.text_area("What's on your mind?", placeholder="Share your learning progress, thoughts, or skill exchange requests...")
        submit_post = st.form_submit_button("Publish Post")
        
        if submit_post and post_content.strip():
            new_item = {
                'author': st.session_state.profile['full_name'],
                'role': st.session_state.profile['title'],
                'time': 'Just now',
                'content': post_content,
                'likes': 0,
                'comments': []
            }
            st.session_state.posts.insert(0, new_item)
            st.success("Post published successfully!")
            st.rerun()

    st.markdown("---")
    st.markdown("### 📰 Community Wall")
    
    for idx, post in enumerate(st.session_state.posts):
        with st.container():
            st.markdown(f"""
                <div class="peer-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div>
                            <strong style="font-size: 16px; color: #1B1F3B;">{post['author']}</strong> 
                            <span style="color: #64748B; font-size: 13px;">— {post['role']}</span>
                        </div>
                        <span style="color: #94A3B8; font-size: 12px;">{post['time']}</span>
                    </div>
                    <p style="color: #334155; font-size: 15px; margin-bottom: 16px;">{post['content']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            col_like, col_comment_count = st.columns([1, 5])
            with col_like:
                if st.button(f"❤️ {post['likes']}", key=f"like_{idx}"):
                    st.session_state.posts[idx]['likes'] += 1
                    st.rerun()
            
            # Comments section
            with st.expander(f"💬 Comments ({len(post['comments'])})"):
                for comment in post['comments']:
                    st.markdown(f"- {comment}")
                
                new_comment = st.text_input("Add a comment...", key=f"comment_input_{idx}")
                if st.button("Reply", key=f"reply_btn_{idx}"):
                    if new_comment.strip():
                        st.session_state.posts[idx]['comments'].append(f"**{st.session_state.profile['full_name']}**: {new_comment}")
                        st.rerun()

# ==========================================
# 2. PEERS PAGE (COMMUNITY DIRECTORY)
# ==========================================
elif st.session_state.selected_page == "👥 Peers Directory":
    # Check if we are viewing a specific peer profile dynamically
    if st.session_state.get('viewing_profile'):
        peer = st.session_state.viewing_profile
        if st.button("← Back to Directory"):
            st.session_state.viewing_profile = None
            st.rerun()
            
        st.title(f"👤 {peer['name']}'s Profile")
        st.markdown(f"### {peer['title']}")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown(f"""
                <div class="peer-card">
                    <h4>Status: <span class="badge-online">{peer['status']}</span></h4>
                    <p>⭐ <b>Rating:</b> {peer['rating']} / 5.0</p>
                    <hr>
                    <b>Skills Offered:</b>
                    <ul>
                        {''.join([f"<li>{s}</li>" for s in peer['skills']])}
                    </ul>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("### About & Exchange Sessions")
            st.write(f"{peer['name']} is an active member of PeerHub specializing in collaborative skill exchange. Book a session or initiate a direct chat to start learning together!")
            if st.button("💬 Start Direct Chat", key=f"chat_with_{peer['id']}"):
                st.session_state.selected_page = "💬 Chats & Direct Hub"
                st.rerun()
    else:
        st.title("👥 Community Directory")
        st.markdown("Discover active peers, filter by skills, and collaborate on exchange sessions.")
        
        search_query = st.text_input("🔍 Search peers by name or skill...", "").lower()
        
        filtered_peers = [
            p for p in st.session_state.peers 
            if search_query in p['name'].lower() or any(search_query in s.lower() for s in p['skills']) or search_query in p['title'].lower()
        ]
        
        cols = st.columns(2)
        for i, peer in enumerate(filtered_peers):
            with cols[i % 2]:
                status_class = "badge-online" if peer['status'] == "Online" else ("badge-session" if peer['status'] == "In a session" else "badge-away")
                st.markdown(f"""
                    <div class="peer-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h3 style="margin: 0; color: #1B1F3B;">{peer['name']}</h3>
                            <span class="{status_class}">{peer['status']}</span>
                        </div>
                        <p style="color: #64748B; margin: 4px 0 12px 0;">{peer['title']} • ⭐ {peer['rating']}</p>
                        <div style="margin-bottom: 12px;">
                            {' '.join([f'<span style="background: #E0F2FE; color: #0369A1; padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 500; margin-right: 4px;">{s}</span>' for s in peer['skills']])}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"View Profile & Connect", key=f"view_peer_{peer['id']}"):
                    st.session_state.viewing_profile = peer
                    st.rerun()

# ==========================================
# 3. CHATS (INSTAGRAM/SNAPCHAT STYLE)
# ==========================================
elif st.session_state.selected_page == "💬 Chats & Direct Hub":
    st.title("💬 Chats & Direct Hub")
    
    chat_names = list(st.session_state.chats.keys())
    selected_chat = st.selectbox("Select Conversation Thread", chat_names)
    
    # Dual-pane layout: Chat on left, Shared resources on right
    chat_col, resource_col = st.columns([2, 1])
    
    with chat_col:
        st.markdown(f"### 💬 Conversation with {selected_chat}")
        
        # Chat box container
        chat_container = st.container(height=400)
        with chat_container:
            for msg in st.session_state.chats[selected_chat]:
                alignment = "right" if msg['sender'] == 'Feriel' else "left"
                bg_color = "#0A66C2" if msg['sender'] == 'Feriel' else "#FFFFFF"
                text_color = "#FFFFFF" if msg['sender'] == 'Feriel' else "#1B1F3B"
                border_style = "1px solid #E2E8F0" if msg['sender'] != 'Feriel' else "none"
                
                st.markdown(f"""
                    <div style="text-align: {alignment}; margin-bottom: 10px;">
                        <div style="display: inline-block; background-color: {bg_color}; color: {text_color}; padding: 10px 14px; border-radius: 12px; border: {border_style}; max-width: 75%; text-align: left;">
                            <small style="opacity: 0.8; display: block; font-size: 10px; margin-bottom: 2px;">{msg['sender']} • {msg['time']}</small>
                            {msg['text']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        # Interactive Message Input & Media Options
        user_message = st.text_input("Type a message...", key="chat_msg_input")
        
        col_send, col_video, col_audio, col_voice, col_media = st.columns([2, 1, 1, 1, 1])
        with col_send:
            if st.button("Send Message", use_container_width=True):
                if user_message.strip():
                    st.session_state.chats[selected_chat].append({
                        'sender': 'Feriel',
                        'text': user_message,
                        'time': datetime.now().strftime("%I:%M %p")
                    })
                    st.rerun()
        with col_video:
            if st.button("📹 Video", use_container_width=True):
                st.toast("Initiating simulated Video Call...")
        with col_audio:
            if st.button("📞 Audio", use_container_width=True):
                st.toast("Initiating simulated Audio Call...")
        with col_voice:
            if st.button("🎤 Voice", use_container_width=True):
                st.toast("Voice note recorded and attached!")
        with col_media:
            if st.button("📷 Media", use_container_width=True):
                st.toast("Media attachment dialog opened.")

    with resource_col:
        st.markdown("### 🗂️ Shared Resources")
        st.markdown("""
            <div class="peer-card">
                <b>📌 Pinned Notebooks</b>
                <p style="font-size: 13px; color: #64748B; margin-top: 5px;">Python_Basics_Notes.ipynb</p>
                <hr style="margin: 8px 0;">
                <b>🎨 Shared Design Board</b>
                <p style="font-size: 13px; color: #64748B; margin-top: 5px;">Figma Wireframe Sprint v2</p>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_sketch = st.file_uploader("Upload sketch or document", type=['png', 'jpg', 'pdf'])
        if uploaded_sketch:
            st.success("Resource uploaded to chat successfully!")

# ==========================================
# 4. COURSE SCHEDULE & CALENDAR PAGE
# ==========================================
elif st.session_state.selected_page == "📅 Course Schedule":
    st.title("📅 Course Schedule & Calendar Manager")
    st.markdown("Organize and manage upcoming peer exchange sessions with your learning partners.")
    
    col_sched1, col_sched2 = st.columns([1, 1])
    
    with col_sched1:
        st.markdown("### 🗓️ Book New Session")
        with st.form("booking_form"):
            partner_name = st.selectbox("Select Peer Partner", [p['name'] for p in st.session_state.peers])
            session_topic = st.text_input("Course / Exchange Topic", "Advanced UI Prototyping")
            session_date = st.date_input("Session Date", date.today())
            session_time = st.time_input("Session Time", time(15, 0))
            
            book_btn = st.form_submit_button("Confirm & Schedule Session")
            if book_btn:
                st.session_state.scheduled_sessions.append({
                    'peer': partner_name,
                    'topic': session_topic,
                    'date': str(session_date),
                    'time': str(session_time),
                    'status': 'Confirmed'
                })
                st.success(f"Session successfully booked with {partner_name}!")
                st.rerun()

    with col_sched2:
        st.markdown("### 📋 Your Confirmed Sessions")
        if not st.session_state.scheduled_sessions:
            st.info("No upcoming sessions scheduled.")
        else:
            for s in st.session_state.scheduled_sessions:
                st.markdown(f"""
                    <div class="peer-card">
                        <h4 style="margin: 0; color: #0A66C2;">{s['topic']}</h4>
                        <p style="margin: 4px 0; font-weight: 500;">Partner: {s['peer']}</p>
                        <p style="color: #64748B; font-size: 13px; margin: 0;">📅 {s['date']} at {s['time']} • <span style="color: #059669; font-weight: 600;">{s['status']}</span></p>
                    </div>
                """, unsafe_allow_html=True)

# ==========================================
# 5. MY PROFILE PAGE (STANDARD & STRUCTURED)
# ==========================================
elif st.session_state.selected_page == "👤 My Profile":
    # Top header status & utility bar
    col_top1, col_top2 = st.columns([3, 1])
    with col_top1:
        st.title("👤 My Professional Portfolio")
    with col_top2:
        dark_mode_toggle = st.toggle("Dark/Light Mode", value=False)
        st.markdown("🕒 **Schedule:** Active")

    # Cover banner & Profile avatar section
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0A66C2 0%, #1B1F3B 100%); height: 140px; border-radius: 12px; margin-bottom: -50px;"></div>
    """, unsafe_allow_html=True)
    
    col_avatar, col_info = st.columns([1, 4])
    with col_avatar:
        if st.session_state.profile['avatar']:
            st.image(st.session_state.profile['avatar'], width=110)
        else:
            st.markdown("""
                <div style="width: 110px; height: 110px; background-color: #CBD5E1; border-radius: 50%; border: 4px solid white; display: flex; align-items: center; justify-content: center; font-size: 40px;">
                    👩‍💻
                </div>
            """, unsafe_allow_html=True)
            
        # Camera & Image upload options
        with st.expander("📷 Update Avatar"):
            uploaded_file = st.file_uploader("Upload Profile Picture", type=['png', 'jpg', 'jpeg'])
            if uploaded_file:
                st.session_state.profile['avatar'] = uploaded_file
                st.success("Avatar updated!")
                st.rerun()
            
            camera_image = st.camera_input("Take a picture")
            if camera_image:
                st.session_state.profile['avatar'] = camera_image
                st.success("Camera photo set as avatar!")
                st.rerun()

    with col_info:
        st.markdown(f"### {st.session_state.profile['full_name']}")
        st.markdown(f"**{st.session_state.profile['title']}** • 📍 {st.session_state.profile['location']}")

    st.markdown("---")

    # Analytics Metrics Row
    m1, m2, m3 = st.columns(3)
    m1.metric("Completed Sessions", st.session_state.profile['completed_sessions'], "+2 this week")
    m2.metric("Hour Bank (Credits)", f"{st.session_state.profile['credits']} hrs", "Earn & Redeem")
    m3.metric("Community Rating", f"{st.session_state.profile['rating']} ⭐", "Top 5% Rated")

    st.markdown("---")

    # Editable Bio ("About Me") Section
    st.markdown("### 📝 About Me")
    new_bio = st.text_area("Edit your professional bio", value=st.session_state.profile['bio'])
    if st.button("Save Bio"):
        st.session_state.profile['bio'] = new_bio
        st.success("Bio updated successfully!")

    st.markdown("---")

    # Skills & Expertise with Proficiency Levels
    col_skill1, col_skill2 = st.columns(2)
    with col_skill1:
        st.markdown("### 🛠️ Skills & Expertise")
        for skill, level in st.session_state.profile['skills'].items():
            st.markdown(f"- **{skill}**: `{level}`")
            
        with st.form("add_skill_form"):
            st.markdown("##### Add New Skill")
            new_skill_name = st.text_input("Skill Name")
            new_skill_level = st.selectbox("Proficiency Level", ["Beginner", "Intermediate", "Advanced", "Expert"])
            add_skill_btn = st.form_submit_button("Add Skill")
            if add_skill_btn and new_skill_name.strip():
                st.session_state.profile['skills'][new_skill_name] = new_skill_level
                st.success(f"Added skill: {new_skill_name}!")
                st.rerun()

    with col_skill2:
        st.markdown("### 🏆 Badges Earned")
        badge_html = " ".join([f'<span style="background: #FEF3C7; color: #92400E; padding: 6px 12px; border-radius: 8px; font-weight: 600; display: inline-block; margin: 4px;">{b}</span>' for b in st.session_state.profile['badges']])
        st.markdown(f"<div style='margin-top: 10px;'>{badge_html}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # User's Own Posts Section
    st.markdown("### 📌 My Shared Posts")
    user_posts = [p for p in st.session_state.posts if p['author'] == st.session_state.profile['full_name']]
    if not user_posts:
        st.info("You haven't published any posts yet. Head over to the Home page to share your thoughts!")
    else:
        for up in user_posts:
            st.markdown(f"""
                <div class="peer-card">
                    <small style="color: #64748B;">{up['time']}</small>
                    <p style="margin-top: 6px; color: #1B1F3B;">{up['content']}</p>
                    <small>❤️ {up['likes']} likes • 💬 {len(up['comments'])} comments</small>
                </div>
            """, unsafe_allow_html=True)
