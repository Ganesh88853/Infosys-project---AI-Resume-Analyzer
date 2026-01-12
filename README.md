# 📄 AI Resume Analyzer (Infosys Internship Project)

This project is part of the **Infosys Springboard Internship Program**.  
It helps users upload their resume, extract content, analyze skills using AI, and receive job recommendations.

---

## 🚀 Features

- 🔐 User Authentication (Register/Login)
- 📁 Resume Upload (PDF / DOCX)
- ✨ Automatic Text Extraction
- 📊 Resume Content Preview
- 🎯 AI-Powered Resume Analysis *(Coming in next milestone)*
- 💼 Job Recommendations *(Planned Feature)*
- 🧠 Session Management (User stays logged in)
- 🛢 SQLite database storage

---

## 🧱 Tech Stack

| Component | Technology |
|----------|------------|
| Frontend | Streamlit |
| Backend | Python |
| Database | SQLite |
| Authentication | bcrypt hashing |
| File Parsing | PyPDF2, python-docx |

---

## 📂 Project Structure
resume_app/
│── app.py
│── requirements.txt
│── README.md
│── .gitignore
│── data/
│ └── app.db
│── backend/
│ ├── auth.py
│ └── resume_parser.py
│── frontend/
│ ├── login.py
│ ├── registration.py
│ └── dashboard.py
│── utils/
├── database.py
└── config.py



---

## 🛠 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/USERNAME/Infosys-Project-AI-Resume-Analyzer.git
cd Infosys-Project-AI-Resume-Analyzer

python -m venv venv
venv\Scripts\activate   # Windows

Install Requirements:
pip install -r requirements.txt

Run the Application:
streamlit run app.py

📄 Resume Analyzer & Job Recommendation Platform

An AI-powered resume analysis and job recommendation platform that helps users upload resumes, analyze strengths, scrape jobs, filter relevant opportunities, and receive personalized job recommendations with application tips.

🚀 Project Overview

This project is designed to:

Analyze user resumes using AI

Scrape real job listings (LinkedIn-based)

Filter and rank jobs based on resume relevance

Provide personalized job recommendations

Display results through a clean Streamlit dashboard

The system is built with modular backend logic and a modern Streamlit frontend, allowing future scalability.

🧩 Core Features
✅ Authentication & User Management

User login & registration

Session-based authentication

Secure dashboard access

📄 Resume Upload & Analysis (Task 14)

Upload PDF/DOCX resumes

Extract resume text

AI-based resume analysis

Skill extraction and scoring

Resume improvement suggestions

🌐 Job Scraping Engine (Task 15)

Automated LinkedIn job scraping using Selenium

Extracted data:

Job title

Company

Location

Job URL

Description

Handles pagination and lazy loading

Avoids duplicate job entries

Saves jobs into SQLite database

🎯 Job Filtering Logic (Task 16 – Backend)

Filters jobs based on:

Skill match percentage

Experience level

Location preference

Remote eligibility

Configurable minimum match threshold

Removes irrelevant or duplicate jobs

🧠 Job Recommendation Engine (Task 17 – Backend Logic Mocked)

Ranks jobs using:

Match percentage (primary)

Posted date (secondary)

Applicants count

Categorizes jobs:

Excellent (85–100%)

Good (70–84%)

Fair (60–69%)

Generates personalized application tips:

Skills to highlight

Missing skills

Interview preparation advice

(Currently mocked in frontend, backend-ready)

💼 Job Recommendations Page (Task 18 – Frontend)

Beautiful job cards UI

Match score indicators (progress bar)

Filters:

Location

Job type

Experience level

Match percentage

Sorting:

Best match

Most recent

Fewest applicants

Job actions:

Apply on LinkedIn

Save job

Saved jobs section

Empty-state handling

🖥️ Tech Stack
Frontend

Streamlit

Interactive UI components

Session state management

Backend

Python

SQLite

Selenium (job scraping)

LLM-based analysis (mock-ready)

Modular repository pattern

📁 Project Structure
resume_app/
│
├── backend/
│   ├── auth/
│   ├── scraper/
│   │   ├── job_search.py
│   │   ├── job_details.py
│   │   └── driver_manager.py
│   ├── jobs/
│   │   ├── job_repository.py
│   │   └── job_filter.py
│   ├── database/
│   │   ├── db.py
│   │   └── init_jobs_table.py
│   ├── resume_parser.py
│   ├── resume_scorer.py
│   └── improvement_engine.py
│
├── frontend/
│   ├── dashboard.py
│   ├── analysis.py
│   ├── job_recommendations.py
│   └── job_search_preferences.py
│
├── app.py
├── app.db
├── requirements.txt
└── README.md

▶️ How to Run the Project
1️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Initialize Database
python backend/database/init_jobs_table.py

4️⃣ Run the Application
streamlit run app.py

🧪 Current Status
Task	Status
Resume Upload & Analysis	✅ Completed
Job Scraping	✅ Completed
Job Filtering	✅ Completed
Job Recommendation Engine	🟡 Mocked
Job Recommendations UI	✅ Completed
Saved Jobs	✅ Completed
Backend ↔ Frontend Integration	🔜 In Progress
🔮 Future Enhancements

Full LLM-powered backend recommendation engine

Cover letter generation

Resume-job keyword optimization

Application tracking system

Email/job alerts

Admin dashboard

👨‍💻 Author

Sai Ganesh
AI Resume Analyzer & Job Recommendation Platform
Built as part of a milestone-based full-stack AI project 🚀