from flask import Flask, send_from_directory
from flask_cors import CORS
from userdatabase import init_user_table

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


# Run app

if __name__ == "__main__":
    init_user_table()
    app.run(debug=True)
