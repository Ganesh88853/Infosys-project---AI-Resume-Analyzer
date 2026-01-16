import bcrypt
import streamlit as st

from utils.database import get_user_by_email, save_user, is_valid_email

# Key for storing user session in Streamlit
SESSION_KEY = "auth_user"


# ---------------- REGISTRATION LOGIC ----------------

def register_user(name: str, email: str, password: str) -> tuple[bool, str]:
    """
    Register a new user.
    Returns (success, message).
    """
    # Extra safety validation (UI also validates, but backend must not trust input blindly)
    if not name.strip():
        return False, "Name cannot be empty."

    if not is_valid_email(email):
        return False, "Invalid email format."

    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    # We already hash the password inside save_user()
    # and handle duplicate emails there.
    success, msg = save_user(name, email, password)
    return success, msg


# ---------------- LOGIN LOGIC ----------------

def login_user(email: str, password: str) -> tuple[bool, str, dict | None]:
    """
    Login user by verifying password against hashed value in DB.
    Returns (success, message, user_dict or None).
    """
    if not is_valid_email(email):
        return False, "Please enter a valid email address.", None

    row = get_user_by_email(email)
    if not row:
        # user not found
        return False, "Invalid email or password.", None

    user_id, name, email_db, password_hash, created_at = row

    # password_hash is stored as bytes (BLOB), so we verify using bcrypt
    if not bcrypt.checkpw(password.encode("utf-8"), password_hash):
        return False, "Invalid email or password.", None

    user = {
        "id": user_id,
        "name": name,
        "email": email_db,
        "created_at": created_at,
    }
    return True, "Login successful.", user


# ---------------- SESSION MANAGEMENT ----------------

def start_session(user: dict):
    """Store logged-in user in Streamlit session_state."""
    st.session_state[SESSION_KEY] = user


def get_current_user() -> dict | None:
    """Return current logged-in user dict or None."""
    return st.session_state.get(SESSION_KEY)


def is_logged_in() -> bool:
    """Check if any user is logged in."""
    return SESSION_KEY in st.session_state and st.session_state[SESSION_KEY] is not None


def logout_user():
    """Clear the logged-in user from session."""
    if SESSION_KEY in st.session_state:
        del st.session_state[SESSION_KEY]
