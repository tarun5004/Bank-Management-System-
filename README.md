# Bank Management System

A modern banking application built with Python featuring both a command-line interface and a Streamlit web interface. The system provides essential banking operations with secure PIN hashing and persistent JSON data storage.

## 🎯 Project Overview

This Bank Management System is a full-featured application that simulates core banking functionalities. The system supports account creation, deposits, withdrawals, account management, and secure authentication with data persistence through JSON file storage.

## ✨ Features

### Core Banking Operations
- **📝 Account Creation** - Register with name, age, email, and secure PIN
- **💰 Deposit** - Add funds to your account (up to ₹100,000 per transaction)
- **💸 Withdraw** - Withdraw funds with balance verification
- **📊 View Details** - Check account information with masked PIN
- **✏️ Update Details** - Modify name, email, or PIN
- **🗑️ Delete Account** - Close account with confirmation

### Security Features
- 🔐 SHA-256 PIN hashing (PINs are never stored in plain text)
- 🛡️ Input validation (email format, PIN length, age verification)
- 🔒 Session management for web interface
- 👁️ Masked account numbers in logs

### User Interfaces
- **Web Interface** - Modern Streamlit-based UI with intuitive navigation
- **CLI Interface** - Traditional command-line interface for terminal users

## 🛠️ Technologies & Libraries

| Library | Purpose |
|---------|---------|
| `streamlit` | Web application framework |
| `json` | Data serialization and persistence |
| `hashlib` | Secure PIN hashing (SHA-256) |
| `re` | Email validation regex |
| `random` | Account number generation |
| `pathlib` | Cross-platform file handling |
| `typing` | Type hints for code clarity |

## 📁 Project Structure

```
Bank-Management-System-/
├── app.py              # Streamlit web application
├── bank.py             # Refactored Bank class with all operations
├── main.py             # Legacy CLI application
├── data.json           # JSON database (auto-generated)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/tarun5004/Bank-Management-System-.git
   cd Bank-Management-System-
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Running the Application

### Web Interface (Streamlit)

```bash
streamlit run app.py
```

This will start a local web server and open the application in your default browser at `http://localhost:8501`.

### Command-Line Interface

```bash
python bank.py
```

Or use the legacy CLI:
```bash
python main.py
```

## 📖 Usage Guide

### Web Interface Navigation

1. **Home** - Welcome page with feature overview
2. **Create Account** - Fill in the form with:
   - Full name (letters and spaces only)
   - Age (minimum 18 years)
   - Valid email address
   - 4-digit PIN
3. **Deposit/Withdraw** - Login with account number and PIN
4. **Account Details** - View your account information
5. **Update Details** - Modify your profile
6. **Delete Account** - Close your account (requires confirmation)

### CLI Menu Options

```
Press 1 For Creating an account
Press 2 for Depositing the Money in the bank
Press 3 For Withdrawing the money
Press 4 for details
Press 5 for updating details
Press 6 for deleting your account
```

## 📊 Data Structure

### Account Object Schema
```json
{
    "name": "string",
    "age": "integer",
    "email": "string (validated format)",
    "pin": "string (SHA-256 hash)",
    "accountNo": "string (8 characters)",
    "balance": "float"
}
```

## 🔧 API Reference

### Bank Class Methods

| Method | Description |
|--------|-------------|
| `create_account(name, age, email, pin)` | Create a new account |
| `deposit(account_no, pin, amount)` | Deposit funds |
| `withdraw(account_no, pin, amount)` | Withdraw funds |
| `get_details(account_no, pin)` | Get account details |
| `update_details(account_no, pin, ...)` | Update account info |
| `delete_account(account_no, pin)` | Delete account |

### Validation Methods

| Method | Description |
|--------|-------------|
| `validate_email(email)` | Check email format |
| `validate_pin(pin)` | Check PIN is 4 digits |
| `validate_name(name)` | Check name format |
| `validate_age(age)` | Check age ≥ 18 |

### Custom Exceptions

| Exception | When Raised |
|-----------|-------------|
| `ValidationError` | Invalid input data |
| `AccountNotFoundError` | Account doesn't exist |
| `AuthenticationError` | Wrong PIN |
| `InsufficientFundsError` | Not enough balance |

## 🔐 Security Best Practices

1. **Never share your PIN** - It's securely hashed and cannot be recovered
2. **Save your account number** - Required for all transactions
3. **Use a unique PIN** - Don't reuse PINs from other services
4. **Logout after use** - Especially on shared computers

## 🧪 Development

### Running Tests (if applicable)
```bash
python -m pytest tests/
```

### Code Style
The project follows PEP 8 guidelines with:
- Type hints for all function parameters and returns
- Docstrings for all classes and methods
- Constants for magic numbers

## 📝 Version History

- **v2.0** - Added Streamlit web interface, PIN hashing, and full CRUD operations
- **v1.0** - Initial CLI version with basic account creation and deposits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

**Tarun** - [GitHub Profile](https://github.com/tarun5004)

---

**Built with ❤️ using Python and Streamlit**