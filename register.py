# User Registration - Signin / Signup (refactored for web use)
from customer import *
from bank import Bank
import random


def signup(username, password, name, age, city):
    """Register a new user. Returns dict with success/failure info."""
    temp = db_query(f"SELECT username FROM customers where username = '{username}';")
    if temp:
        return {"success": False, "message": "Username already exists. Please choose another."}

    # Generate unique account number
    while True:
        account_number = int(random.randint(10000000, 99999999))
        temp = db_query(f"SELECT account_number FROM customers WHERE account_number = '{account_number}';")
        if not temp:
            break

    cobj = Customer(username, password, name, age, city, account_number)
    cobj.createuser()
    bobj = Bank(username, account_number)
    bobj.create_transaction_table()
    return {"success": True, "account_number": account_number, "message": "Account created successfully!"}


def signin(username, password):
    """Authenticate a user. Returns dict with success/failure info."""
    temp = db_query(f"SELECT username FROM customers where username = '{username}';")
    if not temp:
        return {"success": False, "message": "Username not found. Please sign up."}

    stored = db_query(f"SELECT password FROM customers where username = '{username}';")
    if stored[0][0] == password:
        acc = db_query(f"SELECT account_number FROM customers WHERE username = '{username}';")
        return {"success": True, "username": username, "account_number": acc[0][0], "message": "Signed in successfully."}
    else:
        return {"success": False, "message": "Incorrect password. Please try again."}
