import sqlite3

DATABASE = "users.db"

# Connect to Database

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Create Users Table

def init_user_table():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_id TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
        """
    )
    conn.commit()
    conn.close()

# Create New User

def create_user(name, student_id, email, password):
    conn = get_db_connection()

    existing = conn.execute(
        "SELECT * FROM users WHERE student_id = ? OR email = ?",
        (student_id, email),
    ).fetchone()

    if existing:
        conn.close()
        return False

    conn.execute(
        """
        INSERT INTO users (name, student_id, email, password)
        VALUES (?, ?, ?, ?)
        """,
        (name, student_id, email, password),
    )
    conn.commit()
    conn.close()
    return True


# Validate Login

def validate_login(student_id, password):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE student_id = ? AND password = ?",
        (student_id, password),
    ).fetchone()
    conn.close()
    return user
