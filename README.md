# Bank Management System

Welcome to the Bank Management System, a Python-based command-line application designed to manage bank accounts efficiently. This system allows users to sign in, sign up, manage their accounts, perform transactions, and check their account details.

## Features

- **Sign In / Sign Up**
  - Check if User is Registered
  - No User Registration

- **Account Management**
  - Same Account
    - Credit / Withdraw
    - Send Money to Another Account
  - Account Details Update
  - Transaction History

- **Banking Facilities**
  - Account Details
  - Registration
  - Account Management
  - Transaction History
  - Balance Enquiry
  - Credit / Withdraw
  - Funds Transfer
  - Date/Time Functions
  - OOPs Implementation
  - Separate Account Number

## Getting Started

### Prerequisites

Ensure you have Python 3.8+ installed. Recommended: create a virtual environment.

### Installation & Run (Unix / WSL)

1. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Copy the example environment and edit values as needed:
```bash
cp .env.example .env
# edit .env and set DATABASE_URL and SECRET_KEY
```
4. Initialize the database schema:
```bash
python database.py
```
5. Run the Flask app:
```bash
python app.py
```

### Installation & Run (Windows PowerShell)

1. Create and activate a virtual environment:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
2. Install dependencies:
```powershell
pip install -r requirements.txt
```
3. Copy `.env.example` to `.env` and set values (or set environment variables):
```powershell
copy .env.example .env
# edit .env with a text editor and set DATABASE_URL and SECRET_KEY
```
4. Initialize the database schema:
```powershell
python database.py
```
5. Run the app:
```powershell
python app.py
```

### Notes

- This project uses PostgreSQL (psycopg2). `DATABASE_URL` should be a valid Postgres connection string.
- The app reads environment variables via `python-dotenv`. Keep your production secrets out of version control.
- Development: the app runs on port 5000 by default.

## Detailed Features

### Registration

- New users can register by providing personal details and creating an account.

### Sign In / Sign Up

- Users can sign in using their account credentials.
- New users can sign up and create a new account.

### Account Management

- Update account details.
- View and manage the transaction history.
- Enquire about account balance.

### Transactions

- Credit or withdraw money from the account.
- Transfer funds to another account.

### Banking Facilities

- Provides various banking functionalities like balance enquiry, funds transfer, and viewing transaction history.
- Implements object-oriented programming (OOP) for better code management and scalability.
- Each account has a unique account number.

### Date/Time Functions

- Utilizes date and time functions to keep track of transactions and account activities.

## Contributing

We welcome contributions to enhance the features and improve the system. Feel free to fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any queries or issues, please reach out to us through our social media channels:

- [YouTube](https://www.youtube.com/@itsmohitcodes)
- [Telegram](https://t.me/itsmohitcodes)
- [Instagram](https://www.instagram.com/itsmohit.codes)
- [LinkedIn](https://www.linkedin.com/in/itsmohitprajapat/)

Thank you for using the Bank Management System! We hope it helps you manage your bank accounts effectively.
