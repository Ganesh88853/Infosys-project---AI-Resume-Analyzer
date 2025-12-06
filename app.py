import streamlit as st

from utils.database import init_db
from frontend.registration import registration_page
from frontend.login import login_page
from frontend.dashboard import dashboard_page
from backend.auth import is_logged_in, get_current_user, logout_user

st.set_page_config(page_title="AI Resume App", page_icon="🧾")

# Make sure DB & tables exist
init_db()


def main():
    # Default page
    if "page" not in st.session_state:
        st.session_state["page"] = "login"

    st.sidebar.title("AI Resume App")

    if is_logged_in():
        user = get_current_user()
        st.sidebar.success(f"Logged in as: {user['name']}")

        choice = st.sidebar.radio("Menu", ["Dashboard", "Logout"])

        if choice == "Dashboard":
            dashboard_page()
        elif choice == "Logout":
            logout_user()
            st.session_state["page"] = "login"
            st.rerun()

    else:
        # Not logged in: can choose Login or Register
        choice = st.sidebar.radio("Menu", ["Login", "Register"])

        if choice == "Login":
            st.session_state["page"] = "login"
            login_page()
        else:
            st.session_state["page"] = "register"
            registration_page()


if __name__ == "__main__":
    main()
