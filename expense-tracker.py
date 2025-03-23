import streamlit as st
import requests

# URL of your Flask authentication server
AUTH_SERVER = "http://127.0.0.1:5000"

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = None

# Function to check login status
def check_login():
    try:
        response = requests.get(AUTH_SERVER)
        if "Hello" in response.text:
            st.session_state.logged_in = True
            st.session_state.user_email = response.text.split(",")[0].split(" ")[1]
        else:
            st.session_state.logged_in = False
    except:
        st.session_state.logged_in = False

# Function to handle login
def login():
    st.write("Redirecting to login...")
    st.markdown(f'<meta http-equiv="refresh" content="0;URL={AUTH_SERVER}/login">', unsafe_allow_html=True)

# Function to handle logout
def logout():
    st.session_state.logged_in = False
    st.session_state.user_email = None
    requests.get(AUTH_SERVER + "/logout")
    st.success("Logged out successfully!")
    st.experimental_rerun()

# Check if user is logged in
check_login()

# If not logged in, show login button
if not st.session_state.logged_in:
    st.title("🔑 Login to Expense Tracker")
    st.button("Login with Amazon Cognito", on_click=login)
else:
    st.sidebar.write(f"Logged in as {st.session_state.user_email}")
    st.sidebar.button("🚪 Logout", on_click=logout)

    # Display sidebar and main menu options
    st.sidebar.title("📌 Main Menu")
    if st.sidebar.button("📊 Dashboard"):
        st.session_state.page = "Dashboard"
    if st.sidebar.button("📂 Upload Receipt"):
        st.session_state.page = "Upload"
    if st.sidebar.button("📄 Report"):
        st.session_state.page = "Report"
    if st.sidebar.button("🤖 Chatbot"):
        st.session_state.page = "Chatbot"

    # Page Navigation
    if st.session_state.page == "Dashboard":
        st.title("📈 Dashboard")
        st.write("Welcome to your Expense Tracker dashboard!")
    elif st.session_state.page == "Upload":
        st.title("📂 Upload Receipt")
        uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "pdf"])
        if uploaded_file:
            st.success("File uploaded successfully!")
    elif st.session_state.page == "Report":
        st.title("📄 Report")
        st.write("View your expense reports here.")
    elif st.session_state.page == "Chatbot":
        st.title("🤖 Chatbot")
        st.write("Interact with the chatbot here.")
