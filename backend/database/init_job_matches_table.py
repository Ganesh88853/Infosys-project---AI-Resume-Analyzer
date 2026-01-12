from pathlib import Path
import sqlite3


# --------------------------------------------------
# DATABASE PATH
# --------------------------------------------------
DB_PATH = Path(__file__).resolve().parents[2] / "app.db"


def get_db_connection():
    return sqlite3.connect(DB_PATH)

def init_job_preferences_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            job_title TEXT NOT NULL,
            locations TEXT,
            preferred_companies TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("✅ job_preferences table created successfully")



def load_search_history():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT job_title, created_at
        FROM job_preferences
        ORDER BY created_at DESC
        LIMIT 5
    """)

    rows = cur.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    init_job_preferences_table()
