import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "app.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH)


def save_job(job):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
                       INSERT INTO jobs (job_title, company, location, job_url,
                                         description, employment_type,
                                         job_type, experience_level, remote, posted_date)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       """, (
                           job["title"],
                           job["company"],
                           job["location"],
                           job["url"],
                           job["description"],
                           job.get("employment_type"),
                           job.get("job_type"),
                           job.get("experience_level"),
                           int(job.get("remote", False)),
                           job.get("posted_date")
                       ))

        conn.commit()
        return "saved"

    except sqlite3.IntegrityError:
        return "duplicate"

    except Exception as e:
        print("❌ DB ERROR:", e)
        return "error"

    finally:
        conn.close()
