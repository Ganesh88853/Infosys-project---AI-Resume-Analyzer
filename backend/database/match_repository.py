from pathlib import Path
import sqlite3
import json

# --------------------------------------------------
# DATABASE PATH
# --------------------------------------------------
DB_PATH = Path(__file__).resolve().parents[1] / "app.db"


def get_db_connection():
    return sqlite3.connect(DB_PATH)


def save_job_match(job_id, user_id, score, explanation):
    """
    Saves job match score & explanation into job_matches table
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO job_matches (
            job_id,
            user_id,
            match_score,
            skill_match,
            experience_match,
            education_match,
            responsibility_match,
            match_reason,
            application_status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        job_id,
        user_id,
        score,
        explanation.get("skill_match", 0),
        explanation.get("experience_match", 0),
        explanation.get("education_match", 0),
        explanation.get("responsibility_match", 0),
        json.dumps(explanation),
        "Not Applied"
    ))

    conn.commit()
    conn.close()


def get_matches_for_user(user_id):
    """
    Used by frontend Job Recommendations page
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            j.id,
            j.job_title,
            j.company,
            j.location,
            j.job_url,
            j.description,
            jm.match_score,
            jm.match_reason
        FROM jobs j
        JOIN job_matches jm ON jm.job_id = j.id
        WHERE jm.user_id = ?
        ORDER BY jm.match_score DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return rows
