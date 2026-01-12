import streamlit as st
from datetime import datetime, timedelta

# --------------------------------------------------
# MOCK BACKEND OUTPUT (Task 17 Simulation)
# --------------------------------------------------
def job_recommendation_page(jobs=None):
    MOCK_RECOMMENDATIONS = [
        {
            "id": 1,
            "title": "Data Analyst Intern",
            "company": "Google",
            "location": "Bangalore",
            "job_type": "Internship",
            "experience_level": "Entry",
            "match_score": 92,
            "posted_date": datetime.now() - timedelta(days=1),
            "salary": "6–8 LPA",
            "applicants": 32,
            "job_url": "https://linkedin.com",
            "matching_skills": ["Python", "SQL", "Data Analysis"],
            "missing_skills": ["Power BI"],
            "application_tips": [
                "Emphasize Python projects",
                "Mention SQL joins & queries",
                "Prepare dashboard examples"
            ]
        },
        {
            "id": 2,
            "title": "Junior Data Scientist",
            "company": "Amazon",
            "location": "Remote",
            "job_type": "Full-time",
            "experience_level": "Entry",
            "match_score": 85,
            "posted_date": datetime.now(),
            "salary": "10–12 LPA",
            "applicants": 120,
            "job_url": "https://linkedin.com",
            "matching_skills": ["Machine Learning", "Python"],
            "missing_skills": ["Deep Learning"],
            "application_tips": [
                "Highlight ML internships",
                "Explain model evaluation clearly",
                "Prepare behavioral questions"
            ]
        },
        {
            "id": 3,
            "title": "Business Analyst",
            "company": "Deloitte",
            "location": "Hyderabad",
            "job_type": "Full-time",
            "experience_level": "Mid",
            "match_score": 72,
            "posted_date": datetime.now() - timedelta(days=4),
            "salary": "8–10 LPA",
            "applicants": 85,
            "job_url": "https://linkedin.com",
            "matching_skills": ["Excel", "SQL"],
            "missing_skills": ["Tableau"],
            "application_tips": [
                "Show business case studies",
                "Explain stakeholder handling",
                "Brush up Excel functions"
            ]
        },
        {
            "id": 4,
            "title": "AI Research Intern",
            "company": "Microsoft",
            "location": "Bangalore",
            "job_type": "Internship",
            "experience_level": "Entry",
            "match_score": 95,
            "posted_date": datetime.now(),
            "salary": "Stipend",
            "applicants": 20,
            "job_url": "https://linkedin.com",
            "matching_skills": ["Python", "ML", "Research"],
            "missing_skills": ["Paper Writing"],
            "application_tips": [
                "Highlight research projects",
                "Explain ML theory clearly",
                "Prepare GitHub portfolio"
            ]
        }
    ]

    # --------------------------------------------------
    # SESSION STATE
    # --------------------------------------------------

    if "saved_jobs" not in st.session_state:
        st.session_state.saved_jobs = []

    # --------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------
    st.title("💼 Job Recommendations")
    
    st.caption("Personalized opportunities ranked just for you")

    # --------------------------------------------------
    # SUMMARY STATS
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    avg_match = round(sum(j["match_score"] for j in MOCK_RECOMMENDATIONS) / len(MOCK_RECOMMENDATIONS))

    col1.metric("Total Jobs Found", len(MOCK_RECOMMENDATIONS))
    col2.metric("Average Match Score", f"{avg_match}%")
    col3.metric(
        "New Jobs Today",
        len([j for j in MOCK_RECOMMENDATIONS if (datetime.now() - j["posted_date"]).days == 0])
    )

    st.divider()

    # --------------------------------------------------
    # SIDEBAR FILTERS
    # --------------------------------------------------

    st.sidebar.header("🔍 Filters")

    min_match = st.sidebar.slider("Minimum Match %", 60, 100, 60)
    locations = st.sidebar.multiselect(
        "Location",
        options=list(set(j["location"] for j in MOCK_RECOMMENDATIONS))
    )
    job_types = st.sidebar.multiselect(
        "Job Type",
        ["Full-time", "Part-time", "Contract", "Internship"]
    )
    experience_levels = st.sidebar.multiselect(
        "Experience Level",
        ["Entry", "Mid", "Senior"]
    )

    sort_option = st.sidebar.selectbox(
        "Sort By",
        ["Best Match", "Most Recent", "Highest Salary", "Fewest Applicants"]
    )

    # --------------------------------------------------
    # FILTER + SORT LOGIC
    # --------------------------------------------------

    filtered_jobs = []

    for job in MOCK_RECOMMENDATIONS:
        if job["match_score"] < min_match:
            continue
        if locations and job["location"] not in locations:
            continue
        if job_types and job["job_type"] not in job_types:
            continue
        if experience_levels and job["experience_level"] not in experience_levels:
            continue
        filtered_jobs.append(job)

    if sort_option == "Best Match":
        filtered_jobs.sort(key=lambda x: x["match_score"], reverse=True)
    elif sort_option == "Most Recent":
        filtered_jobs.sort(key=lambda x: x["posted_date"], reverse=True)
    elif sort_option == "Fewest Applicants":
        filtered_jobs.sort(key=lambda x: x["applicants"])
    elif sort_option == "Highest Salary":
        filtered_jobs.sort(key=lambda x: x["salary"], reverse=True)

    # --------------------------------------------------
    # BEST MATCHES DISPLAY
    # --------------------------------------------------

    st.subheader("⭐ Best Matches")

    if not filtered_jobs:
        st.warning("No jobs found. Try adjusting your filters.")
    else:
        for job in filtered_jobs[:10]:
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown(f"### {job['title']}")
                    st.write(f"🏢 *{job['company']}*")
                    st.write(f"📍 {job['location']} | 💼 {job['job_type']}")
                    st.progress(job["match_score"] / 100)
                    st.caption(f"Match Score: {job['match_score']}%")

                with col2:
                    if st.button("💾 Save", key=f"save_{job['id']}"):
                        st.session_state.saved_jobs.append(job)
                    st.link_button("Apply", job["job_url"])

                with st.expander("View Details"):
                    st.write("*Matching Skills:*", ", ".join(job["matching_skills"]))
                    st.write("*Missing Skills:*", ", ".join(job["missing_skills"]))
                    st.info("📌 Application Tips:")
                    for tip in job["application_tips"]:
                        st.write(f"- {tip}")

    # --------------------------------------------------
    # SAVED JOBS TAB
    # --------------------------------------------------

    st.divider()
    st.subheader("📌 Saved Jobs")

    if not st.session_state.saved_jobs:
        st.info("No saved jobs yet.")
    else:
        for job in st.session_state.saved_jobs:
            st.write(f"🔖 {job['title']} at {job['company']}")