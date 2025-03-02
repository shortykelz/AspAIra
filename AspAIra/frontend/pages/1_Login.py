import streamlit as st
import requests

# Initialize session states if not exists
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'

# Page configuration
st.set_page_config(
    page_title="AspAIra - Login",
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
    
    .form-container {
        width: 100%;
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background-color: #f8f9fa;
        border-radius: 8px;
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
    
    /* Hide problematic elements */
    [data-baseweb="select"] > div[aria-hidden="true"] {
        display: none !important;
    }
    
    /* Form field styles */
    .stTextInput > div > div > input {
        font-size: 1rem !important;
    }
    
    .form-row {
        margin-bottom: 1rem;
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
        
        .form-container {
            border: 1px solid ButtonText !important;
            background-color: Canvas !important;
            color: CanvasText !important;
        }
        
        .stTextInput > div > div > input {
            border-color: ButtonText !important;
            background-color: Field !important;
            color: FieldText !important;
        }
        
        .logo {
            color: CanvasText !important;
        }
    }
</style>
""", unsafe_allow_html=True)

def login(username: str, password: str):
    try:
        response = requests.post(
            "http://localhost:8000/token",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None

def create_account(username: str, password: str):
    try:
        response = requests.post(
            "http://localhost:8000/signup",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            return True
        return False
    except requests.RequestException:
        return False

def check_profile_status(token: str):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get("http://localhost:8000/user/profile-status", headers=headers)
        if response.status_code == 200:
            return response.json()
        return {"profile1_complete": False, "profile2_complete": False}
    except requests.RequestException:
        return {"profile1_complete": False, "profile2_complete": False}

# Main container with semantic HTML
st.markdown('<main class="main-container">', unsafe_allow_html=True)

# Back button with proper labeling
st.markdown('<div class="button-container">', unsafe_allow_html=True)
if st.button(
    "← Back to Home",
    key="back_button",
    help="Return to the main page",
    use_container_width=True,
    type="primary"
):
    st.switch_page("Home.py")
st.markdown('</div>', unsafe_allow_html=True)

# Logo and Title
st.markdown('<h1 class="logo">🌱 AspAIra</h1>', unsafe_allow_html=True)

# Login form with proper labeling
with st.form("login_form", clear_on_submit=True):
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    st.markdown('<div class="form-row">', unsafe_allow_html=True)
    username = st.text_input(
        "Username",
        key="username",
        autocomplete="username",
        help="Enter your username",
        placeholder="Enter your username"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-row">', unsafe_allow_html=True)
    password = st.text_input(
        "Password",
        type="password",
        key="password",
        autocomplete="current-password",
        help="Enter your password",
        placeholder="Enter your password"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        login_button = st.form_submit_button(
            "Sign In",
            use_container_width=True,
            help="Sign in to your account"
        )
    with col2:
        signup_button = st.form_submit_button(
            "Create Account",
            use_container_width=True,
            help="Create a new account"
        )

    if login_button and username and password:
        result = login(username, password)
        if result:
            st.session_state.access_token = result["access_token"]
            # Check profile status
            profile_status = check_profile_status(result["access_token"])
            st.session_state.profile_status = profile_status
            
            if not profile_status["profile1_complete"]:
                st.success("Login successful! Please complete your profile.")
                st.switch_page("pages/2_Profile1.py")
            elif not profile_status["profile2_complete"]:
                st.success("Login successful! Please complete your financial profile.")
                st.switch_page("pages/2_Profile2.py")
            else:
                st.success("Login successful!")
                st.switch_page("pages/3_Coach_Landing.py")
        else:
            st.error("Invalid username or password")

    if signup_button and username and password:
        if create_account(username, password):
            result = login(username, password)  # Auto-login after signup
            if result:
                st.session_state.access_token = result["access_token"]
                st.session_state.profile_status = {"profile1_complete": False, "profile2_complete": False}
                st.success("Account created successfully! Please complete your profile.")
                st.switch_page("pages/2_Profile1.py")
        else:
            st.error("Username already exists or error creating account")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</main>', unsafe_allow_html=True) 