import streamlit as st
import requests
from urllib.parse import urljoin

# Configuration
API_BASE_URL = "http://localhost:8000/api/"

st.set_page_config(
    page_title="AispAIra - Profile Setup",
    page_icon="👤",
    layout="wide"
)

# Income ranges
INCOME_RANGES = [
    "Under $30,000",
    "$30,000 - $50,000",
    "$50,000 - $75,000",
    "$75,000 - $100,000",
    "$100,000 - $150,000",
    "Over $150,000"
]

# Financial goals
FINANCIAL_GOALS = [
    "Retirement Planning",
    "Investment Growth",
    "Debt Reduction",
    "Emergency Fund",
    "Home Purchase",
    "Education Savings",
    "Business Investment"
]

# Risk tolerance levels
RISK_TOLERANCE = [
    "Conservative",
    "Moderately Conservative",
    "Moderate",
    "Moderately Aggressive",
    "Aggressive"
]

# Investment experience
INVESTMENT_EXPERIENCE = [
    "None",
    "Beginner",
    "Intermediate",
    "Advanced",
    "Expert"
]

# Investment types
INVESTMENT_TYPES = [
    "Stocks",
    "Bonds",
    "Mutual Funds",
    "ETFs",
    "Real Estate",
    "Cryptocurrencies",
    "Commodities"
]

def update_profile(profile_data: dict) -> bool:
    try:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.post(
            urljoin(API_BASE_URL, "users/profile"),
            json=profile_data,
            headers=headers
        )
        return response.status_code == 200
    except requests.RequestException:
        return False

def main():
    if not st.session_state.get("authenticated"):
        st.switch_page("pages/1_Login.py")
        
    st.title("👤 Profile Setup")
    st.markdown("""
    Please tell us more about yourself so we can provide personalized financial guidance.
    """)
    
    with st.form("profile_form"):
        income_range = st.selectbox(
            "What is your annual income range?",
            options=INCOME_RANGES
        )
        
        financial_goals = st.multiselect(
            "What are your financial goals? (Select all that apply)",
            options=FINANCIAL_GOALS
        )
        
        risk_tolerance = st.select_slider(
            "What is your risk tolerance level?",
            options=RISK_TOLERANCE
        )
        
        investment_experience = st.radio(
            "What is your investment experience level?",
            options=INVESTMENT_EXPERIENCE
        )
        
        preferred_investments = st.multiselect(
            "What investment types interest you? (Select all that apply)",
            options=INVESTMENT_TYPES
        )
        
        submit = st.form_submit_button("Continue to Financial Coaching")
        
        if submit:
            if not financial_goals or not preferred_investments:
                st.error("Please select at least one financial goal and investment type.")
            else:
                profile_data = {
                    "income_range": income_range,
                    "financial_goals": financial_goals,
                    "risk_tolerance": risk_tolerance,
                    "investment_experience": investment_experience,
                    "preferred_investment_types": preferred_investments
                }
                
                if update_profile(profile_data):
                    st.session_state.profile_completed = True
                    st.success("Profile updated successfully!")
                    st.switch_page("pages/3_Financial_Coaching.py")
                else:
                    st.error("Failed to update profile. Please try again.")

if __name__ == "__main__":
    main() 