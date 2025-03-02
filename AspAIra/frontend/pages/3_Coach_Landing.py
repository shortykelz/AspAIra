import streamlit as st

# Initialize session states
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'coach_landing'
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'current_module' not in st.session_state:
    st.session_state.current_module = None

# Page configuration
st.set_page_config(
    page_title="AspAIra - Financial Coach",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS
st.markdown("""
<style>
    /* Hide Streamlit elements */
    [data-testid="collapsedControl"] {display: none !important;}
    section[data-testid="stSidebar"] {display: none !important;}
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    
    /* Block analytics */
    iframe[src*="analytics"], iframe[src*="segment"],
    script[src*="analytics"], script[src*="segment"],
    div[data-testid="stGoogleAnalytics"] {
        display: none !important;
    }
    
    /* Main styles */
    .stApp {
        max-width: 100%;
        padding: 1rem;
    }
    
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 1rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .logo {
        font-size: 2rem;
        margin-bottom: 2rem;
        color: #000000;
    }
    
    /* Button styles */
    .stButton > button {
        width: 100% !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        border-radius: 8px !important;
        background-color: #FF4B4B !important;
        color: white !important;
        border: 2px solid transparent !important;
        cursor: pointer !important;
        transition: background-color 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #E63E3E !important;
    }
    
    .stButton > button:focus {
        outline: 2px solid #000000 !important;
        outline-offset: 2px !important;
    }
    
    /* Module styles */
    .module-container {
        width: 100%;
        max-width: 600px;
        margin: 2rem auto;
        padding: 2rem;
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    
    .module-row {
        margin-bottom: 1.5rem;
    }
    
    /* Navigation styles */
    .nav-container {
        width: 100%;
        max-width: 600px;
        margin: 2rem auto;
        display: flex;
        justify-content: space-between;
        gap: 1rem;
    }
    
    .nav-item {
        flex: 1;
    }
    
    /* Chat container */
    .chat-container {
        width: 100%;
        max-width: 600px;
        margin: 2rem auto;
        padding: 2rem;
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    
    /* Hide problematic elements */
    [data-baseweb="select"] > div[aria-hidden="true"] {
        display: none !important;
    }
    
    @media (forced-colors: active) {
        .stButton > button {
            border: 2px solid ButtonText !important;
            background-color: ButtonFace !important;
            color: ButtonText !important;
        }
        
        .stButton > button:hover,
        .stButton > button:focus {
            border-color: Highlight !important;
            background-color: ButtonFace !important;
            color: Highlight !important;
        }
        
        .module-container,
        .chat-container {
            border: 1px solid ButtonText !important;
            background-color: Canvas !important;
            color: CanvasText !important;
        }
        
        .logo,
        h2, h3, p {
            color: CanvasText !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Main container with semantic HTML
st.markdown('<main class="main-container">', unsafe_allow_html=True)

# Back button with proper labeling
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button("← Back", key="back_button", help="Return to the previous page"):
    st.session_state.current_page = 'profile2'
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Logo and Title
st.markdown('<h1 class="logo">🌱 AspAIra</h1>', unsafe_allow_html=True)

# Welcome message
st.markdown("""
<div class="module-container">
    <h2>Welcome to Your Financial Journey!</h2>
    <p>Let's work together to achieve your financial goals.</p>
</div>
""", unsafe_allow_html=True)

# Learning modules section
st.markdown('<div class="module-container">', unsafe_allow_html=True)

st.markdown('<h3>Learning Modules</h3>', unsafe_allow_html=True)

st.markdown('<div class="module-row">', unsafe_allow_html=True)
if st.button(
    "📊 Budgeting Basics",
    key="budgeting_module",
    help="Learn the fundamentals of creating and managing a budget",
    use_container_width=True
):
    st.session_state.current_module = 'budgeting'
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="module-row">', unsafe_allow_html=True)
if st.button(
    "💰 Smart Saving",
    key="saving_module",
    help="Discover effective strategies for saving money",
    use_container_width=True
):
    st.session_state.current_module = 'saving'
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="module-row">', unsafe_allow_html=True)
if st.button(
    "🏦 Banking & Remittance",
    key="banking_module",
    help="Learn about banking services and sending money home safely",
    use_container_width=True
):
    st.session_state.current_module = 'banking'
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# AI Assistant chat section
st.markdown("""
<div class="chat-container">
    <h3>Your AI Financial Assistant</h3>
    <p>Have questions? I'm here to help! Ask me anything about personal finance.</p>
</div>
""", unsafe_allow_html=True)

# Bottom navigation
st.markdown('<div class="nav-container">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="nav-item">', unsafe_allow_html=True)
    if st.button(
        "👩‍🏫 Coach",
        key="nav_coach",
        help="Return to the coach dashboard",
        use_container_width=True
    ):
        st.session_state.current_page = 'coach_landing'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="nav-item">', unsafe_allow_html=True)
    if st.button(
        "👤 Profile",
        key="nav_profile",
        help="View and edit your profile",
        use_container_width=True
    ):
        st.session_state.current_page = 'profile1'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="nav-item">', unsafe_allow_html=True)
    if st.button(
        "💬 Chat",
        key="nav_chat",
        help="Chat with your AI financial assistant",
        use_container_width=True
    ):
        st.session_state.current_page = 'chat'
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</main>', unsafe_allow_html=True) 