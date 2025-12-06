import os
import re
import sqlite3
from datetime import datetime

import bcrypt

# Path to our SQLite database file
DB_PATH = os.path.join("data", "app.db")


def init_db():
    """
    Create the database file and the tables if they do not exist.
    Call this once at app startup.
    """
    # Ensure data folder exists
    os.makedirs("data", exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        # USERS TABLE
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash BLOB NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            """
        )

        # Index on email for faster lookup
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);"
        )

        # RESUMES TABLE (to store uploaded resume & extracted text)
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                file_name TEXT NOT NULL,
                extracted_text TEXT NOT NULL,
                uploaded_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            );
            """
        )

        # Index for faster lookup by user
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_resumes_user_id ON resumes(user_id);"
        )

        conn.commit()


# ------------- VALIDATION HELPERS -------------

EMAIL_REGEX = re.compile(r"^[^@]+@[^@]+\.[^@]+$")


def is_valid_email(email: str) -> bool:
    """Return True if email looks valid."""
    return bool(email) and EMAIL_REGEX.match(email) is not None


# ------------- USERS CRUD -------------


def save_user(name: str, email: str, password: str) -> tuple[bool, str]:
    """
    Save a new user in the database.

    Returns (success, message)
    """
    if not is_valid_email(email):
        return False, "Invalid email format."

    if not name.strip():
        return False, "Name cannot be empty."

    # Hash the password
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO users (name, email, password_hash, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (name.strip(), email.lower().strip(), password_hash, datetime.utcnow().isoformat()),
        )
        conn.commit()
        return True, "User registered successfully."
    except sqlite3.IntegrityError:
        # UNIQUE constraint failed: users.email
        return False, "Email already exists. Please use a different email."
    except Exception as e:
        return False, f"Unexpected error: {e}"
    finally:
        try:
            conn.close()
        except Exception:
            pass


def get_user_by_email(email: str):
    """Fetch one user row by email, or None if not found."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id, name, email, password_hash, created_at FROM users WHERE email = ?",
                (email.lower().strip(),))
    row = cur.fetchone()
    conn.close()
    return row


# ------------- RESUME HELPERS -------------


def save_resume_for_user(user_id: int, file_name: str, extracted_text: str) -> tuple[bool, str]:
    """
    Save resume text for a user.
    Returns (success, message).
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO resumes (user_id, file_name, extracted_text, uploaded_at)
            VALUES (?, ?, ?, datetime('now'))
            """,
            (user_id, file_name, extracted_text),
        )
        conn.commit()
        return True, "Resume saved successfully."
    except Exception as e:
        return False, f"Error saving resume: {e}"
    finally:
        try:
            conn.close()
        except Exception:
            pass


def get_latest_resume_for_user(user_id: int):
    """
    Get the most recently uploaded resume for a user.
    Returns a row tuple (id, user_id, file_name, extracted_text, uploaded_at) or None.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, user_id, file_name, extracted_text, uploaded_at
        FROM resumes
        WHERE user_id = ?
        ORDER BY uploaded_at DESC
        LIMIT 1
        """,
        (user_id,),
    )
    row = cur.fetchone()
    conn.close()
    return row


def delete_latest_resume_for_user(user_id: int) -> tuple[bool, str]:
    """
    Delete the most recent resume for a user.
    Returns (success, message).
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute(
            """
            DELETE FROM resumes
            WHERE id = (
                SELECT id FROM resumes
                WHERE user_id = ?
                ORDER BY uploaded_at DESC
                LIMIT 1
            )
            """,
            (user_id,),
        )
        conn.commit()
        return True, "Latest resume deleted."
    except Exception as e:
        return False, f"Error deleting resume: {e}"
    finally:
        try:
            conn.close()
        except Exception:
            pass
