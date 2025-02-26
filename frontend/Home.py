import streamlit as st

st.set_page_config(
    page_title="AispAIra - Your AI Financial Coach",
    page_icon="💰",
    layout="wide"
)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def main():
    st.title("Welcome to AispAIra 💰")
    
    st.markdown("""
    ## Your Personal AI Financial Coach
    
    AispAIra is your intelligent financial companion, designed to help you make smarter financial decisions
    and achieve your financial goals. With personalized guidance and expert insights, we're here to support
    your financial journey.
    
    ### What We Offer:
    - 📊 Personalized Financial Planning
    - 💡 Smart Investment Guidance
    - 📈 Goal-based Recommendations
    - 🎯 Custom Strategy Development
    """)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if not st.session_state.authenticated:
            st.button("Create Your Profile", 
                     use_container_width=True,
                     type="primary",
                     help="Click to start your financial journey",
                     on_click=lambda: st.switch_page("pages/1_Login.py"))

if __name__ == "__main__":
    main() 