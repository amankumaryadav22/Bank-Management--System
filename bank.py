# Bank Services
from database import *
import datetime


class Bank:
    def __init__(self, username, account_number):
        self.__username = username
        self.__account_number = account_number

    def create_transaction_table(self):
        db_query(f"CREATE TABLE IF NOT EXISTS {self.__username}_transaction "
                 f"( timedate VARCHAR(30),"
                 f"account_number INTEGER,"
                 f"remarks VARCHAR(30),"
                 f"amount INTEGER )")

    def balanceequiry(self):
        temp = db_query(
            f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        return temp[0][0]

    def deposit(self, amount):
        temp = db_query(
            f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        new_balance = amount + temp[0][0]
        db_query(
            f"UPDATE customers SET balance = '{new_balance}' WHERE username = '{self.__username}'; ")
        db_query(f"INSERT INTO {self.__username}_transaction VALUES ("
                 f"'{datetime.datetime.now()}',"
                 f"'{self.__account_number}',"
                 f"'Amount Deposit',"
                 f"'{amount}'"
                 f")")
        return {"success": True, "balance": new_balance, "message": "Amount deposited successfully."}

    def withdraw(self, amount):
        temp = db_query(
            f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        current_balance = temp[0][0]
        if amount > current_balance:
            return {"success": False, "balance": current_balance, "message": "Insufficient balance. Please deposit money."}
        new_balance = current_balance - amount
        db_query(
            f"UPDATE customers SET balance = '{new_balance}' WHERE username = '{self.__username}'; ")
        db_query(f"INSERT INTO {self.__username}_transaction VALUES ("
                 f"'{datetime.datetime.now()}',"
                 f"'{self.__account_number}',"
                 f"'Amount Withdraw',"
                 f"'{amount}'"
                 f")")
        return {"success": True, "balance": new_balance, "message": "Amount withdrawn successfully."}

    def fundtransfer(self, receive, amount):
        temp = db_query(
            f"SELECT balance FROM customers WHERE username = '{self.__username}';")
        current_balance = temp[0][0]
        if amount > current_balance:
            return {"success": False, "balance": current_balance, "message": "Insufficient balance. Please deposit money."}
        temp2 = db_query(
            f"SELECT balance FROM customers WHERE account_number = '{receive}';")
        if temp2 == []:
            return {"success": False, "balance": current_balance, "message": "Recipient account number does not exist."}
        new_balance_sender = current_balance - amount
        new_balance_receiver = amount + temp2[0][0]
        db_query(
            f"UPDATE customers SET balance = '{new_balance_sender}' WHERE username = '{self.__username}'; ")
        db_query(
            f"UPDATE customers SET balance = '{new_balance_receiver}' WHERE account_number = '{receive}'; ")
        receiver_username = db_query(
            f"SELECT username FROM customers where account_number = '{receive}';")
        db_query(f"INSERT INTO {receiver_username[0][0]}_transaction VALUES ("
                 f"'{datetime.datetime.now()}',"
                 f"'{self.__account_number}',"
                 f"'Fund Transfer From {self.__account_number}',"
                 f"'{amount}'"
                 f")")
        db_query(f"INSERT INTO {self.__username}_transaction VALUES ("
                 f"'{datetime.datetime.now()}',"
                 f"'{self.__account_number}',"
                 f"'Fund Transfer -> {receive}',"
                 f"'{amount}'"
                 f")")
        return {"success": True, "balance": new_balance_sender, "message": f"₹{amount} transferred successfully to account {receive}."}
