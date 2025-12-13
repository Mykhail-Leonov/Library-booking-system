from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from userdatabase import init_user_table, create_user, validate_login


from bookingdatabase import (
    init_booking_table,
    TIME_SLOTS,
    get_allowed_dates,
    get_month_summary,
    get_booked_slots,
    create_booking
)


app = Flask(__name__, static_folder="static")
CORS(app)


# HTML Routes

@app.route("/")
def serve_main():
    return send_from_directory("static", "main.html")

@app.route("/login")
def serve_login():
    return send_from_directory("static", "login.html")

@app.route("/register")
def serve_register():
    return send_from_directory("static", "register.html")

@app.route("/static/<path:path>")
def serve_static(path):
    return send_from_directory("static", path)


# Registration API

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    name = data.get("name", "").strip()
    student_id = data.get("student_id", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not name or not student_id or not email or not password:
        return jsonify({"error": "All fields are required."}), 400
    
    if len(student_id) != 8:
        return jsonify({"error": "Student ID must be 8 digits."}), 400

    if "@bradfordcollege.ac.uk" not in email:
        return jsonify({"error": "Email must be a valid college email."}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    success = create_user(name, student_id, email, password)

    if not success:
        return jsonify({"error": "Student ID or email already registered."}), 409

    return jsonify({"message": "User registered successfully!"}), 201


# Login API

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    student_id = data.get("student_id", "").strip()
    password = data.get("password", "").strip()

    if not student_id or not password:
        return jsonify({"error": "Student ID and password are required."}), 400

    user = validate_login(student_id, password)

    if not user:
        return jsonify({"error": "Invalid Student ID or password."}), 401

    return jsonify({
        "message": "Login successful!",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "student_id": user["student_id"],
            "email": user["email"]
        }
    }), 200

# Booking APIs
@app.route("/api/bookings/month")
def booking_month():
    booth = request.args["booth"]
    year = int(request.args["year"])
    month = int(request.args["month"])

    return jsonify({
        "summary": get_month_summary(booth, year, month),
        "allowed_dates": list(get_allowed_dates()),
        "time_slots": TIME_SLOTS,
        "total_slots": len(TIME_SLOTS)
    })

@app.route("/api/bookings/slots")
def booking_slots():
    return jsonify({
        "booked_slots": get_booked_slots(
            request.args["booth"],
            request.args["date"]
        ),
        "time_slots": TIME_SLOTS
    })

@app.route("/api/bookings", methods=["POST"])
def booking_create():
    data = request.get_json()
    ok, msg = create_booking(
        data["user_id"],
        data["building"],
        data["booth"],
        data["date"],
        data["time_slot"]
    )
    if not ok:
        return jsonify({"error": msg}), 409
    return jsonify({"message": msg})



# Run app

if __name__ == "__main__":
    init_user_table()
    init_booking_table()
    app.run(debug=True)
