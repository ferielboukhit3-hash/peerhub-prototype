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
            st.session_state.posts.insert(0, new
