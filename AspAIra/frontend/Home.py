import streamlit as st

# Initialize session states
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'language' not in st.session_state:
    st.session_state.language = 'English'
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'home'

# Page configuration
st.set_page_config(
    page_title="AspAIra",
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
    
    .main-image {
        max-width: 100%;
        margin: 1rem 0;
        border-radius: 10px;
    }
    
    .mission-text {
        font-size: 1.1rem;
        line-height: 1.6;
        margin: 1rem 0;
        color: #000000;
    }
    
    /* Button container */
    .button-container {
        width: 100%;
        max-width: 300px;
        margin: 1rem auto;
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
    
    /* Language selector styles */
    .language-selector {
        width: 100%;
        max-width: 400px;
        margin: 2rem auto;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 8px;
    }
    
    .language-label {
        display: block;
        margin-bottom: 0.5rem;
        font-weight: 500;
        color: #000000;
    }
    
    /* Hide problematic elements */
    [data-baseweb="select"] > div[aria-hidden="true"] {
        display: none !important;
    }
    
    /* Ensure select box is visible and accessible */
    .stSelectbox {
        width: 100% !important;
    }
    
    .stSelectbox > div {
        width: 100% !important;
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
        
        .language-selector {
            border: 1px solid ButtonText !important;
            background-color: Canvas !important;
            color: CanvasText !important;
        }
        
        .language-label {
            color: CanvasText !important;
        }
        
        .mission-text {
            color: CanvasText !important;
        }
        
        .logo {
            color: CanvasText !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Main container with semantic HTML
st.markdown('<main class="main-container">', unsafe_allow_html=True)

# Logo and Title with semantic heading
st.markdown('<h1 class="logo">🌱 AspAIra</h1>', unsafe_allow_html=True)

# Main image with proper alt text and title
st.image(
    "https://images.unsplash.com/photo-1512075135822-67cdd9dd7314",
    caption="Empowering Domestic Workers in Dubai",
    use_container_width=True,
)

# Mission Statement with semantic paragraph
st.markdown(
    '<p class="mission-text">'
    'Here to Empower you! Our mission is to empower you with AI-driven financial '
    'literacy education to help you navigate the financial ecosystem in the UAE, '
    'break out of debt cycle, increase savings, and build a stable financial '
    'future as you adjust to life in the UAE.'
    '</p>',
    unsafe_allow_html=True
)

# Sign In Button with proper labeling and container
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button(
    "Sign In to AspAIra",
    key="signin_button",
    help="Access your personal financial assistant",  # Title attribute
    use_container_width=True,
    type="primary"
):
    st.switch_page("pages/1_Login.py")
st.markdown('</div>', unsafe_allow_html=True)

# Language Selection with proper labeling
st.markdown('<div class="language-selector">', unsafe_allow_html=True)
st.markdown('<label for="language-select">Select Your Language / Piliin ang Iyong Wika</label>', unsafe_allow_html=True)
language = st.selectbox(
    label="",  # Empty label since we're using custom label
    options=["English", "Tagalog"],
    key="language-select",  # Matches the 'for' attribute in label
    label_visibility="collapsed",
    help="Choose your preferred language"  # Title attribute
)
st.session_state.language = language
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</main>', unsafe_allow_html=True) 