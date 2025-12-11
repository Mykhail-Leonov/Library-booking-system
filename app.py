from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from userdatabase import init_user_table, create_user, validate_login

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


# Run app

if __name__ == "__main__":
    init_user_table()
    app.run(debug=True)
