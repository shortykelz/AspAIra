import streamlit as st
import requests
from urllib.parse import urljoin

# Configuration
API_BASE_URL = "http://localhost:8000/api/"

st.set_page_config(
    page_title="AispAIra - Financial Coaching",
    page_icon="📊",
    layout="wide"
)

# Financial topics
FINANCIAL_TOPICS = {
    "Investment Basics": [
        "Understanding Stock Markets",
        "Bond Investment Strategies",
        "ETFs vs Mutual Funds",
        "Risk Management",
        "Portfolio Diversification"
    ],
    "Retirement Planning": [
        "401(k) and IRA Basics",
        "Retirement Income Strategies",
        "Social Security Planning",
        "Estate Planning",
        "Healthcare in Retirement"
    ],
    "Debt Management": [
        "Debt Reduction Strategies",
        "Credit Score Improvement",
        "Loan Consolidation",
        "Mortgage Planning",
        "Student Loan Management"
    ],
    "Personal Finance": [
        "Budgeting Basics",
        "Emergency Fund Planning",
        "Tax Planning",
        "Insurance Needs",
        "Real Estate Investment"
    ]
}

def get_profile():
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(
            urljoin(API_BASE_URL, "users/profile"),
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None

def main():
    if not st.session_state.get("authenticated"):
        st.switch_page("pages/1_Login.py")
    
    profile = get_profile()
    if not profile:
        st.error("Failed to load profile. Please try again.")
        st.stop()
    
    st.title("📊 Financial Coaching")
    
    # Welcome message
    st.markdown(f"""
    ## Welcome to Your Personal Financial Coaching Session!
    
    Based on your profile, we've customized our coaching topics to match your:
    - Income Range: {profile.get('income_range')}
    - Risk Tolerance: {profile.get('risk_tolerance')}
    - Investment Experience: {profile.get('investment_experience')}
    """)
    
    st.markdown("---")
    
    # Topic selection
    st.subheader("Select a Topic to Explore")
    
    col1, col2 = st.columns(2)
    
    selected_category = None
    selected_topic = None
    
    with col1:
        st.markdown("### Categories")
        for category in FINANCIAL_TOPICS.keys():
            if st.button(category, use_container_width=True):
                st.session_state.selected_category = category
    
    with col2:
        st.markdown("### Topics")
        if hasattr(st.session_state, 'selected_category'):
            category = st.session_state.selected_category
            topics = FINANCIAL_TOPICS[category]
            for topic in topics:
                if st.button(topic, use_container_width=True):
                    st.session_state.selected_topic = topic
    
    st.markdown("---")
    
    # Display selected topic content
    if hasattr(st.session_state, 'selected_topic'):
        st.subheader(f"📚 {st.session_state.selected_topic}")
        st.markdown("""
        Your personalized coaching content will appear here, tailored to your profile and preferences.
        This section will be integrated with your AI coaching system to provide dynamic, personalized content.
        """)
        
        st.button("Continue to Next Topic", use_container_width=True)

if __name__ == "__main__":
    main() 