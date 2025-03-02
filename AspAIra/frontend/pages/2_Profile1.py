import streamlit as st
import requests
import json

# Check if user is logged in
if 'access_token' not in st.session_state:
    st.switch_page("pages/1_Login.py")

# Page configuration
st.set_page_config(
    page_title="AspAIra - Profile",
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
        forced-color-adjust: none;
    }
    
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 1rem;
        max-width: 800px;
        margin: 0 auto;
        forced-color-adjust: none;
    }
    
    .logo {
        font-size: 2rem;
        margin-bottom: 2rem;
        color: #000000;
        forced-color-adjust: none;
    }
    
    /* Progress bar container */
    .progress-container {
        width: 100%;
        max-width: 600px;
        margin: 1rem auto;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 8px;
        text-align: center;
        forced-color-adjust: none;
    }
    
    /* Form container */
    .form-container {
        width: 100%;
        max-width: 600px;
        margin: 2rem auto;
        padding: 2rem;
        background-color: #f8f9fa;
        border-radius: 8px;
        forced-color-adjust: none;
    }
    
    /* Button container */
    .button-container {
        width: 100%;
        max-width: 300px;
        margin: 1rem auto;
        forced-color-adjust: none;
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
        forced-color-adjust: none !important;
    }
    
    .stButton > button:hover {
        background-color: #E63E3E !important;
    }
    
    .stButton > button:focus {
        outline: 2px solid #000000 !important;
        outline-offset: 2px !important;
    }
    
    /* Form field styles */
    .form-row {
        margin-bottom: 1rem;
        forced-color-adjust: none;
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
            forced-color-adjust: none !important;
        }
        
        .stButton > button:hover,
        .stButton > button:focus {
            border-color: Highlight !important;
            background-color: ButtonFace !important;
            color: Highlight !important;
        }
        
        .form-container,
        .progress-container {
            border: 1px solid ButtonText !important;
            background-color: Canvas !important;
            color: CanvasText !important;
            forced-color-adjust: none !important;
        }
        
        .logo {
            color: CanvasText !important;
            forced-color-adjust: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)

def update_profile(data):
    try:
        headers = {
            "Authorization": f"Bearer {st.session_state.access_token}",
            "Content-Type": "application/json"
        }
        st.write("Sending data:", data)  # Debug print
        response = requests.post(
            "http://localhost:8000/user/profile1",
            json=data,
            headers=headers
        )
        st.write("Response status:", response.status_code)  # Debug print
        st.write("Response text:", response.text)  # Debug print
        return response.status_code == 200, response.text
    except Exception as e:
        st.write("Error:", str(e))  # Debug print
        return False, str(e)

# Main container with semantic HTML
st.markdown('<main class="main-container">', unsafe_allow_html=True)

# Logo and Title
st.markdown('<h1 class="logo">🌱 AspAIra</h1>', unsafe_allow_html=True)

# Progress indicator
st.markdown('<div class="progress-container">', unsafe_allow_html=True)
st.progress(0.5)
st.markdown('<p>Step 1 of 2: Personal Information</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.title("Personal Information")
st.progress(0.5)
st.write("Step 1 of 2")

# Initialize session state for form fields if not exists
if 'profile1_data' not in st.session_state:
    st.session_state.profile1_data = {}

# Form container with proper form handling
with st.form("profile1"):
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    country_of_origin = st.selectbox(
        "Country of Origin",
        ["", "Filipino", "Kenyan", "Sri Lankan"]
    )
    
    time_in_uae = st.selectbox(
        "Time in UAE",
        ["", "Less than a year", "1-3 years", "3-5 years", "5-10 years", "10+ years"]
    )
    
    job_title = st.selectbox(
        "Job Title",
        ["", "Live In maid", "Live out maid", "Cook", "Nanny"]
    )
    
    housing = st.selectbox(
        "Housing",
        ["", "Live In", "Live Out", "Temporary Housing"]
    )
    
    education_level = st.selectbox(
        "Education Level",
        ["", "None", "Primary school", "High school", "College"]
    )
    
    dependents = st.selectbox(
        "Number of Dependents",
        ["", "None", "1", "2", "3", "More than 3"]
    )
    
    data = {
        'country_of_origin': country_of_origin,
        'time_in_uae': time_in_uae,
        'job_title': job_title,
        'housing': housing,
        'education_level': education_level,
        'number_of_dependents': dependents
    }
    
    st.write("Current values:", data)
    
    submitted = st.form_submit_button("Next Step")
    
    if submitted:
        if "" in data.values():
            st.error("Please fill all fields")
        else:
            success, message = update_profile(data)
            if success:
                st.session_state.profile1_data = data
                st.session_state.profile1_complete = True
                st.success("Profile saved!")
                st.switch_page("pages/2_Profile2.py")
            else:
                st.error(f"Error: {message}")

st.markdown('</div>', unsafe_allow_html=True)  # Close form container
st.markdown('</main>', unsafe_allow_html=True)  # Close main container 