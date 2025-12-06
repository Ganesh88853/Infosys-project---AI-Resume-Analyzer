import streamlit as st

from backend.auth import get_current_user, is_logged_in, logout_user
from backend.resume_parser import (
    extract_and_save_resume,
    get_latest_resume_for_user,
    delete_latest_resume_for_user,
)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def _format_size(num_bytes: int) -> str:
    """Return human readable file size."""
    if num_bytes < 1024:
        return f"{num_bytes} B"
    elif num_bytes < 1024 * 1024:
        return f"{num_bytes / 1024:.1f} KB"
    else:
        return f"{num_bytes / (1024 * 1024):.1f} MB"


def _logout_and_rerun():
    logout_user()
    st.session_state["page"] = "login"
    st.rerun()


def dashboard_page():
    """Main dashboard screen after login."""
    # --- Session check ---
    if not is_logged_in():
        st.warning("You must be logged in to view the dashboard.")
        st.session_state["page"] = "login"
        st.rerun()
        return

    user = get_current_user()

    # ----- Header with welcome + logout -----
    header_col1, header_col2 = st.columns([3, 1])
    with header_col1:
        st.subheader(f"Welcome back, {user['name']} 👋")
        st.caption("This is your central hub to manage resumes, analysis, and job recommendations.")
    with header_col2:
        st.button("Logout", type="secondary", on_click=_logout_and_rerun)

    st.markdown("---")

    # ----- Sidebar navigation (session-based) -----
    if "dashboard_section" not in st.session_state:
        st.session_state["dashboard_section"] = "Overview"

    with st.sidebar:
        st.header("Dashboard Menu")
        section = st.radio(
            "Go to",
            ["Overview", "My Profile", "Upload Resume", "Resume Analysis", "Job Recommendations", "Settings"],
            index=["Overview", "My Profile", "Upload Resume", "Resume Analysis", "Job Recommendations", "Settings"].index(
                st.session_state["dashboard_section"]
            ),
        )
        st.session_state["dashboard_section"] = section

    # ----- Fetch quick data from DB for stats -----
    resume_row = get_latest_resume_for_user(user["id"])
    if resume_row:
        resume_id, user_id, file_name, extracted_text, uploaded_at = resume_row
        resume_status = "Uploaded ✅"
        last_resume_date = uploaded_at
    else:
        file_name = None
        extracted_text = ""
        resume_status = "Not uploaded ❌"
        last_resume_date = "N/A"

    # For now, we don't have real analysis or job rec data in DB, so placeholders:
    last_analysis_date = "Not analyzed yet"
    job_reco_count = 0

    # ----- Overview section: Quick Stats + Recent Activity + CTA cards -----
    if section == "Overview":
        st.markdown("### Quick Stats")

        stat_col1, stat_col2, stat_col3 = st.columns(3)
        with stat_col1:
            st.metric("Resume Status", resume_status)
        with stat_col2:
            st.metric("Last Resume Upload", last_resume_date)
        with stat_col3:
            st.metric("Job Recommendations", job_reco_count)

        st.markdown("### Recent Activity")
        if resume_row:
            st.write(f"- 📄 Last resume uploaded: **{file_name}** at **{uploaded_at}**")
            st.write("- 📊 Resume analysis not yet implemented (will be added in next milestone).")
            st.write("- 💼 Job recommendations feature coming soon.")
        else:
            st.write("- No recent activity yet. Upload your first resume to get started.")

        st.markdown("### Next Steps")

        c1, c2 = st.columns(2)

        with c1:
            st.info("📄 **Upload your resume** to enable analysis and job recommendations.")
            if st.button("Go to Upload Resume", key="cta_upload"):
                st.session_state["dashboard_section"] = "Upload Resume"
                st.rerun()

        with c2:
            st.info("🤖 **Resume Analysis** will use AI to score and improve your resume.")
            if st.button("View Resume Analysis (coming soon)", key="cta_analysis"):
                st.session_state["dashboard_section"] = "Resume Analysis"
                st.rerun()

    # ----- My Profile -----
    elif section == "My Profile":
        st.markdown("### My Profile")
        st.write(f"**Name:** {user['name']}")
        st.write(f"**Email:** `{user['email']}`")
        st.write(f"**Account created at:** {user.get('created_at', 'N/A')}")
        st.info("In future, you can add options here to edit profile, change password, etc.")

    # ----- Upload Resume -----
    elif section == "Upload Resume":
        st.markdown("### Upload Resume")
        st.write("Upload your latest resume in PDF or DOCX format.")

        uploaded_file = st.file_uploader(
            "Choose a file (max 5 MB)",
            type=["pdf", "docx"],
        )

        if uploaded_file is not None:
            st.write(f"**File name:** {uploaded_file.name}")
            st.write(f"**File size:** {_format_size(uploaded_file.size)}")

            if uploaded_file.size > MAX_FILE_SIZE:
                st.error("File is too large. Please upload a file smaller than 5 MB.")
            else:
                if st.button("Save & Extract Text"):
                    success, msg = extract_and_save_resume(user["id"], uploaded_file)
                    if success:
                        st.success(msg)
                        st.session_state["dashboard_section"] = "Resume Analysis"
                        st.rerun()
                    else:
                        st.error(msg
                                    + "  \n\n👉 Please upload a *digital* resume (created in Word/Google Docs/Canva)"
                                    + " instead of a scanned photo PDF for best results."
                                )                       
        else:
            st.info("No file selected yet. Please choose a PDF or DOCX resume.")

    # ----- Resume Analysis (placeholder for now) -----
    elif section == "Resume Analysis":
        st.markdown("### Resume Analysis")
        if not resume_row:
            st.warning("No resume found. Please upload a resume first.")
        else:
            st.write(f"Last uploaded resume: **{file_name}** at **{uploaded_at}**")
            st.info(
                "AI-powered resume analysis (ATS score, strengths, weaknesses, missing skills) "
                "will be implemented in the next milestone."
            )
            with st.expander("Show extracted resume text"):
                st.text_area("Extracted Text", extracted_text, height=300)

    # ----- Job Recommendations (placeholder for now) -----
    elif section == "Job Recommendations":
        st.markdown("### Job Recommendations")
        st.info(
            "This section will show AI-based job recommendations based on your skills and resume content "
            "in upcoming milestones."
        )
        if resume_row:
            st.write("✅ Resume available. Once job recommendation logic is added, this page will show matches here.")
        else:
            st.warning("Please upload a resume first to get job recommendations in future.")

    # ----- Settings -----
    elif section == "Settings":
        st.markdown("### Settings")
        st.info("Here you can manage your data and account preferences.")

        if resume_row:
            st.write(f"Latest stored resume: **{file_name}** (uploaded at {uploaded_at})")
            if st.button("Delete Latest Resume"):
                ok, msg = delete_latest_resume_for_user(user["id"])
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        else:
            st.write("No resume stored yet.")

        st.caption("More settings (notification preferences, theme, etc.) can be added later.")
