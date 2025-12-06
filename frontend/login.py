import streamlit as st
from backend.auth import login_user, is_logged_in, start_session, get_current_user


def login_page():
    st.title("Login 🔐")

    # If already logged in, don't show the form again
    if is_logged_in():
        user = get_current_user()
        st.success(f"You are already logged in as {user['name']}.")
        return

    st.write("Enter your credentials to access the AI Resume App.")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # Only run login logic when button is clicked
    if st.button("Login"):
        success, msg, user = login_user(email, password)

        if success:
            start_session(user)
            st.success(msg)
            st.rerun()   # refresh app to go to Dashboard
        else:
            st.error(msg)

    st.info("Don't have an account?")
    if st.button("Go to Register"):
        st.session_state["page"] = "register"
