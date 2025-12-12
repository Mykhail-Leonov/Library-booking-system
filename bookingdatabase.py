from datetime import date, datetime, timedelta
from userdatabase import get_db_connection

# Booking time slots
TIME_SLOTS = [
    "08:30-10:30",
    "10:30-12:30",
    "12:30-14:30",
    "14:30-16:30"
]
# Create booking table
def init_booking_table():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            building TEXT NOT NULL,
            booth TEXT NOT NULL,
            date TEXT NOT NULL,
            time_slot TEXT NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(booth, date, time_slot)
        )
    """)
    conn.commit()
    conn.close()
