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

