from backend.database.db import get_db_connection
from datetime import datetime

def update_job_status(job_url, status):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE jobs
        SET status = ?, status_updated_at = ?
        WHERE job_url = ?
    """, (status, datetime.now(), job_url))

    conn.commit()
    conn.close()
