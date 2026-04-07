from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from database import db_query
from register import signup, signin
from bank import Bank
import os

app = Flask(__name__)
app.secret_key = "bankapp_secret_key_2024_secure"


# ─── Page Routes ─────────────────────────────────────────────────────────────

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("index"))
    return render_template("dashboard.html")


# ─── Auth API ────────────────────────────────────────────────────────────────

@app.route("/api/signup", methods=["POST"])
def api_signup():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    name = data.get("name", "").strip()
    age = data.get("age", "").strip()
    city = data.get("city", "").strip()

    if not all([username, password, name, age, city]):
        return jsonify({"success": False, "message": "All fields are required."}), 400

    try:
        age = int(age)
    except ValueError:
        return jsonify({"success": False, "message": "Age must be a valid number."}), 400

    result = signup(username, password, name, age, city)
    if result["success"]:
        session["username"] = username
        session["account_number"] = result["account_number"]
        return jsonify(result), 201
    return jsonify(result), 409


@app.route("/api/signin", methods=["POST"])
def api_signin():
    data = request.get_json()
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()

    if not username or not password:
        return jsonify({"success": False, "message": "Username and password are required."}), 400

    result = signin(username, password)
    if result["success"]:
        session["username"] = result["username"]
        session["account_number"] = result["account_number"]
        return jsonify(result), 200
    return jsonify(result), 401


@app.route("/api/signout", methods=["POST"])
def api_signout():
    session.clear()
    return jsonify({"success": True, "message": "Signed out successfully."}), 200


# ─── Protected API ───────────────────────────────────────────────────────────

def get_bank():
    """Helper: return a Bank instance for the current session user."""
    username = session.get("username")
    account_number = session.get("account_number")
    if not username or not account_number:
        return None, None
    return Bank(username, account_number), username


@app.route("/api/dashboard", methods=["GET"])
def api_dashboard():
    bank, username = get_bank()
    if not bank:
        return jsonify({"success": False, "message": "Not authenticated."}), 401

    balance = bank.balanceequiry()
    account_number = session.get("account_number")
    row = db_query(f"SELECT name, city, age FROM customers WHERE username = '{username}';")
    name = row[0][0] if row else username
    city = row[0][1] if row else ""
    age = row[0][2] if row else ""

    return jsonify({
        "success": True,
        "username": username,
        "name": name,
        "city": city,
        "age": age,
        "account_number": account_number,
        "balance": balance
    }), 200


@app.route("/api/deposit", methods=["POST"])
def api_deposit():
    bank, _ = get_bank()
    if not bank:
        return jsonify({"success": False, "message": "Not authenticated."}), 401

    data = request.get_json()
    try:
        amount = int(data.get("amount", 0))
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Please enter a valid positive amount."}), 400

    result = bank.deposit(amount)
    return jsonify(result), 200


@app.route("/api/withdraw", methods=["POST"])
def api_withdraw():
    bank, _ = get_bank()
    if not bank:
        return jsonify({"success": False, "message": "Not authenticated."}), 401

    data = request.get_json()
    try:
        amount = int(data.get("amount", 0))
        if amount <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Please enter a valid positive amount."}), 400

    result = bank.withdraw(amount)
    status = 200 if result["success"] else 400
    return jsonify(result), status


@app.route("/api/transfer", methods=["POST"])
def api_transfer():
    bank, _ = get_bank()
    if not bank:
        return jsonify({"success": False, "message": "Not authenticated."}), 401

    data = request.get_json()
    try:
        receive = int(data.get("account_number", 0))
        amount = int(data.get("amount", 0))
        if amount <= 0 or receive <= 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Please enter a valid account number and amount."}), 400

    if receive == session.get("account_number"):
        return jsonify({"success": False, "message": "Cannot transfer to your own account."}), 400

    result = bank.fundtransfer(receive, amount)
    status = 200 if result["success"] else 400
    return jsonify(result), status


@app.route("/api/transactions", methods=["GET"])
def api_transactions():
    bank, username = get_bank()
    if not bank:
        return jsonify({"success": False, "message": "Not authenticated."}), 401

    rows = db_query(
        f"SELECT timedate, account_number, remarks, amount FROM {username}_transaction ORDER BY timedate DESC LIMIT 20;")
    transactions = [
        {"date": r[0], "account_number": r[1], "remarks": r[2], "amount": r[3]}
        for r in rows
    ]
    return jsonify({"success": True, "transactions": transactions}), 200


# ─── Entry Point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
