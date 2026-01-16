from pathlib import Path
import sqlite3

# --------------------------------------------------
# DATABASE PATH
# --------------------------------------------------
DB_PATH = Path(__file__).resolve().parents[2] / "app.db"


def get_db_connection():
    return sqlite3.connect(DB_PATH)
def init_job_matches_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            job_id INTEGER NOT NULL,

            match_score INTEGER NOT NULL,     -- 0–100

            skill_match INTEGER,
            experience_match INTEGER,
            education_match INTEGER,
            responsibility_match INTEGER,

            match_reason TEXT,                -- LLM / rule-based explanation

            is_saved INTEGER DEFAULT 0,        -- 1 = saved
            application_status TEXT DEFAULT 'Not Applied',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (job_id) REFERENCES jobs(id)
        );
    """)

    conn.commit()
    conn.close()

    print("✅ job_matches table ready")

if __name__ == "__main__":
    init_job_matches_table()
