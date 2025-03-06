import streamlit as st
import requests
import uuid
from datetime import datetime

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
    page_icon="🤖",
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
    
    .stChatMessage {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .stTextInput {
        border-radius: 20px;
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

def initialize_chat_session():
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'first_message' not in st.session_state:
        st.session_state.first_message = True

def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message("user" if message["role"] == "user" else "assistant"):
            st.markdown(message["content"])

def get_user_profile():
    """Get user profile from session state"""
    if not st.session_state.get('user'):
        st.error("Please log in first")
        st.stop()
    
    return {
        "user_id": st.session_state.user.get('id'),
        "profile": {
            # Combine profile parts from session state
            **(st.session_state.get('profile_part1', {})),
            **(st.session_state.get('profile_part2', {}))
        }
    }

async def chat_with_agent(message: str, user_profile: dict):
    """Send message to backend and get response"""
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={
                "message": message,
                "user_id": user_profile["user_id"],
                "session_id": st.session_state.session_id,
                "user_profile": {
                    "number_of_dependents": user_profile["profile"].get("dependents_count"),
                    "remittance_amount": user_profile["profile"].get("monthly_remittance"),
                    "bank_account": user_profile["profile"].get("bank_account_status"),
                    "debt_information": user_profile["profile"].get("debt_status"),
                    "remittance_information": user_profile["profile"].get("remittance_method")
                }
            },
            headers={"Authorization": f"Bearer {st.session_state.access_token}"}
        )
        response.raise_for_status()
        return response.json()["response"]
    except Exception as e:
        st.error(f"Error communicating with the financial coach: {str(e)}")
        return None

def main():
    st.title("💬 Your Financial Coach")
    
    # Initialize session
    initialize_chat_session()
    
    try:
        # Get user profile
        user_profile = get_user_profile()
        
        # Display chat interface
        st.markdown("### Chat with your personal financial coach")
        st.markdown("I'm here to help you learn about budgeting, saving, and managing your money. Let's get started!")
        
        # Display chat history
        display_chat_history()
        
        # Show initial message
        if st.session_state.first_message:
            with st.chat_message("assistant"):
                st.markdown("""Hello! I am your financial education bot. Let's talk about how to create a budget and save money.
                
Would you like to learn about:
1. Creating a budget
2. Saving strategies
3. Tips for sending money home

Please choose a number to continue.""")
                st.session_state.first_message = False
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": """Hello! I am your financial education bot. Let's talk about how to create a budget and save money.
                    
Would you like to learn about:
1. Creating a budget
2. Saving strategies
3. Tips for sending money home

Please choose a number to continue."""
                })
        
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get bot response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = chat_with_agent(prompt, user_profile)
                    if response:
                        st.markdown(response)
                        st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error("Please complete your profile before using the chat feature.")
        if st.button("Go to Profile"):
            st.session_state.current_page = 'profile1'
            st.rerun()

if __name__ == "__main__":
    main() 