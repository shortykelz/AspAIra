import streamlit as st
import requests
from urllib.parse import urljoin

# Configuration
API_BASE_URL = "http://localhost:8000/api/"

st.set_page_config(
    page_title="AispAIra - Login",
    page_icon="🔐",
    layout="wide"
)

def login(email: str, password: str) -> bool:
    try:
        response = requests.post(
            urljoin(API_BASE_URL, "users/token"),
            data={"username": email, "password": password}
        )
        if response.status_code == 200:
            token_data = response.json()
            st.session_state.token = token_data["access_token"]
            st.session_state.authenticated = True
            return True
        return False
    except requests.RequestException:
        return False

def register(email: str, password: str) -> bool:
    try:
        response = requests.post(
            urljoin(API_BASE_URL, "users/register"),
            json={"email": email, "password": password}
        )
        return response.status_code == 200
    except requests.RequestException:
        return False

def main():
    st.title("🔐 Login or Create Account")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if login(email, password):
                    st.success("Login successful!")
                    st.switch_page("pages/2_Profile_Form.py")
                else:
                    st.error("Invalid email or password")
    
    with tab2:
        with st.form("register_form"):
            email = st.text_input("Email", key="register_email")
            password = st.text_input("Password", type="password", key="register_password")
            confirm_password = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Register")
            
            if submit:
                if password != confirm_password:
                    st.error("Passwords do not match")
                elif register(email, password):
                    st.success("Registration successful! Please login.")
                    st.experimental_rerun()
                else:
                    st.error("Registration failed. Please try again.")

if __name__ == "__main__":
    if st.session_state.get("authenticated"):
        st.switch_page("pages/2_Profile_Form.py")
    main() 