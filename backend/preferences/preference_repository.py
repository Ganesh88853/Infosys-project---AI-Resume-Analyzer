from backend.database.db import get_db_connection

def get_latest_preferences():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            job_title,
            locations,
            remote_pref,
            experience_level,
            job_types,
            min_salary,
            include_keywords,
            exclude_keywords
        FROM job_preferences
        ORDER BY created_at DESC
        LIMIT 1
    """)

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "job_title": row[0],
        "locations": row[1].split(",") if row[1] else [],
        "remote_pref": row[2],
        "experience_level": row[3],
        "job_types": row[4].split(",") if row[4] else [],
        "min_salary": row[5],
        "include_keywords": row[6].split(",") if row[6] else [],
        "exclude_keywords": row[7].split(",") if row[7] else [],
    }
