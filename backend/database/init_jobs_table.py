from pathlib import Path
import sqlite3

# --------------------------------------------------
# DATABASE PATH
# --------------------------------------------------
DB_PATH = Path(__file__).resolve().parents[2] / "app.db"


def get_db_connection():
    return sqlite3.connect(DB_PATH)


def init_jobs_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 🔥 Drop old table to avoid schema mismatch
    cursor.execute("DROP TABLE IF EXISTS jobs;")

    # ✅ Create correct jobs table
    cursor.execute("""
        CREATE TABLE jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT,
            company TEXT,
            location TEXT,
            job_url TEXT UNIQUE,
            description TEXT,
            employment_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    conn.close()

    print("✅ jobs table created successfully")


# --------------------------------------------------
# RUN ONCE
# --------------------------------------------------
if __name__ == "__main__":
    init_jobs_table()
