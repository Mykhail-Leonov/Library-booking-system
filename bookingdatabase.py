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

# Allowed dates up to 7 days ahead including today, without weekends.

def get_allowed_dates():
    today = date.today()
    last_day = today + timedelta(days=7)

    allowed = set()
    current = today
    while current <= last_day:
        if current.weekday() < 5:
            allowed.add(current.isoformat())
        current += timedelta(days=1)

    return allowed

# Check if user already has a booking on a given date.
def user_has_booking_on_date(user_id, date_str):
    conn = get_db_connection()
    row = conn.execute(
        "SELECT 1 FROM bookings WHERE user_id=? AND date=? LIMIT 1",
        (user_id, date_str)
    ).fetchone()
    conn.close()
    return row is not None
# Monthly booking summary for a booth.
def get_month_summary(booth, year, month):
    conn = get_db_connection()
    rows = conn.execute(
        """
        SELECT date, COUNT(*) as count
        FROM bookings
        WHERE booth = ? AND date LIKE ?
        GROUP BY date
    """, (booth, f"{year}-{month:02d}-%")).fetchall()
    conn.close()

    summary = {}
    for r in rows:
        summary[r["date"]] = int(r["count"])
    return summary
# Get booked slots for a booth on a specific date.
def get_booked_slots(booth, date_str):
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT time_slot FROM bookings WHERE booth=? AND date=?",
        (booth, date_str)
    ).fetchall()
    conn.close()
    return [r["time_slot"] for r in rows]
# Create a new booking after validations.
def create_booking(user_id, building, booth, date_str, time_slot):
    if time_slot not in TIME_SLOTS:
        return False, "Invalid time slot."

    if date_str not in get_allowed_dates():
        return False, "Date is not allowed."

    if user_has_booking_on_date(user_id, date_str):
        return False, "Only one booking per day is allowed."

    conn = get_db_connection()
    try:
        conn.execute("""
            INSERT INTO bookings (user_id, building, booth, date, time_slot, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, building, booth, date_str, time_slot, datetime.now().isoformat()))
        conn.commit()
        return True, "Booking confirmed."
    except Exception:
        return False, "This slot already booked"
    finally:
        conn.close()




# Retrieve all bookings for a user.
def get_user_bookings(user_id):
    conn = get_db_connection()
    rows = conn.execute(
        """
        SELECT id, building, booth, date, time_slot
        FROM bookings
        WHERE user_id = ?
        ORDER BY date
        """,
        (user_id,)
    ).fetchall()
    conn.close()
    return rows

# Delete a booking by ID.
def delete_booking(booking_id, user_id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM bookings WHERE id = ? AND user_id = ?",
        (booking_id, user_id)
    )
    conn.commit()
    conn.close()
