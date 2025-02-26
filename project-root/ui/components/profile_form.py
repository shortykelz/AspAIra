import streamlit as st

# Set the page title and layout
st.set_page_config(page_title="Aspaira", page_icon="🌿", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
        body {
            background-color: #E6F4EA;
        }
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #3B622C;
        }
        .container {
            background-color: #CDE8C5;
            padding: 2rem;
            border-radius: 15px;
            width: 60%;
            margin: auto;
            box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.1);
        }
        .input-box {
            margin-bottom: 10px;
        }
        .continue-button {
            text-align: center;
        }
        .language-select {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title
st.markdown("<h1 class='title'>Aspaira</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Please Tell Us About Yourself ...</h3>", unsafe_allow_html=True)

# User Information Form
with st.form("user_info_form"):
    first_name = st.text_input("First Name", placeholder="Enter your first name")
    last_name = st.text_input("Last Name", placeholder="Enter your last name")
    gender = st.selectbox("Gender", ["Female", "Male", "Other"])
    marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced", "Widowed"])
    age = st.number_input("Age", min_value=18, max_value=100, step=1)
    number_of_kids = st.number_input("Number of Kids", min_value=0, step=1)
    country_of_origin = st.text_input("Country of Origin", placeholder="Enter your country")
    educational_background = st.text_input("Educational Background", placeholder="Enter your education level")

    # Continue button
    submit_button = st.form_submit_button("Continue")

# Language Selection at the Bottom
st.markdown("""
<div class="language-select">
    <select>
        <option>Site Language: English</option>
        <option>Site Language: العربية</option>
        <option>Site Language: Tagalog</option>
    </select>
</div>
""", unsafe_allow_html=True)
