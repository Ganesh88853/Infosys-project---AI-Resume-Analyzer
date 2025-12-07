import streamlit as st
import re
from utils.database import save_user, is_valid_email

# ---------- REGEX RULES ----------
# Name: only letters and spaces
NAME_REGEX = re.compile(r"^[A-Za-z ]+$")

# Password: at least 8 chars, 1 upper, 1 lower, 1 digit, 1 special
PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$"
)


def registration_page():
    st.title("Create your account Bro ✨")
    st.write("Fill in your details to start using the AI Resume Analysis.")

    left, center, right = st.columns([1, 2, 1])

    with center:
        st.markdown("### Registration Form")

        # ------------ Full Name ------------
        full_name = st.text_input("Full Name")
        name_ok = False
        if full_name:
            if NAME_REGEX.fullmatch(full_name.strip()):
                name_ok = True
                st.caption("✅ Looks good")
            else:
                st.caption(
                    "❌ Name should contain only **letters and spaces** (no numbers or symbols)."
                )

        # ------------ Email Address ------------
        email = st.text_input("Email Address")
        email_ok = False
        if email:
            if is_valid_email(email):
                email_ok = True
                st.caption("✅ Email format looks good")
            else:
                st.caption(
                    "❌ Please enter a valid email (like `example@domain.com`)."
                )

        # ------------ Password ------------
        password = st.text_input("Password", type="password")
        pwd_ok = False
        if password:
            if PASSWORD_REGEX.fullmatch(password):
                pwd_ok = True
                st.caption("✅ Strong password")
            else:
                st.caption(
                    "❌ Password must be **min 8 characters** and include:\n"
                    "- one uppercase letter (A-Z)\n"
                    "- one lowercase letter (a-z)\n"
                    "- one number (0-9)\n"
                    "- one special character (@, #, $, !, %, etc.)"
                )

        # ------------ Confirm Password ------------
        confirm_password = st.text_input("Confirm Password", type="password")
        confirm_ok = False
        if confirm_password:
            if confirm_password == password and password != "":
                confirm_ok = True
                st.caption("✅ Passwords match")
            else:
                st.caption("❌ Passwords do not match")

        st.markdown("---")

        # ------------ Register Button ------------
        if st.button("Register"):
            errors = []

            # Full name checks
            if not full_name.strip():
                errors.append("Full name cannot be empty.")
            elif not name_ok:
                errors.append("Please enter a valid full name (letters and spaces only).")

            # Email checks
            if not email.strip():
                errors.append("Email is required.")
            elif not email_ok:
                errors.append("Please enter a valid email address.")

            # Password checks
            if not password:
                errors.append("Password is required.")
            elif not pwd_ok:
                errors.append(
                    "Password does not meet the required strength rules."
                )

            # Confirm password checks
            if not confirm_password:
                errors.append("Please confirm your password.")
            elif not confirm_ok:
                errors.append("Passwords do not match.")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                ok, msg = save_user(full_name, email, password)
                if ok:
                    st.success("User registered successfully! 🎉 You can go to login page.")
                    st.session_state["page"] = "login"
                else:
                    st.error(msg)

        # ------------ Link to Login ------------
        st.write("")
        st.info("Already have an account?")
        if st.button("Go to Login"):
            st.session_state["page"] = "login"