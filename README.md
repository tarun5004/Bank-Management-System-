# Bank Management System

A command-line based banking application built with Python that provides essential banking operations with persistent data storage using JSON.

## 🎯 Project Overview

This Bank Management System is a console-based application that simulates core banking functionalities. The system allows users to create accounts, manage deposits, and maintain account information with data persistence through JSON file storage.

## 🏗️ Architecture

The application follows an Object-Oriented Programming (OOP) approach with a single `Bank` class that encapsulates all banking operations and data management.

### Class Structure

```
Bank
├── Class Attributes
│   ├── database_path (str): Path to JSON database file
│   └── data (list): In-memory storage for account records
│
├── Private Methods
│   ├── __update_database() - Persists data to JSON file
│   └── __account_number_generator() - Generates unique account numbers
│
└── Public Methods
    ├── Create_account() - Account creation workflow
    └── deposit() - Money deposit functionality
```

## 📋 Features

### 1. **Account Creation**
- User registration with validation
- Age verification (minimum 18 years)
- 4-digit PIN authentication
- Unique account number generation
- Initial balance initialization

### 2. **Deposit Management**
- Account verification via account number and PIN
- Amount validation (0 < amount ≤ 100,000)
- Real-time balance update
- Immediate data persistence

### 3. **Data Persistence**
- Automatic JSON file creation
- Real-time data synchronization
- Error handling for file operations

## 🔧 Technical Implementation

### Core Methods

#### `__update_database()` - Static Method
```python
@staticmethod
def __update_database():
    with open(Bank.database_path, "w") as file:
        file.write(json.dumps(Bank.data, indent=4))
```
**Purpose**: Writes the current state of all accounts to `data.json`  
**Access Level**: Private (name mangling with `__`)  
**Return Type**: None

#### `__account_number_generator()` - Class Method
```python
@classmethod
def __account_number_generator(cls):
    alpha = random.choices(string.ascii_letters, k=3)
    digit = random.choices(string.digits, k=3)
    special_char = random.choices("!@#$%^&*()", k=2)
    id = alpha + digit + special_char
    random.shuffle(id)
    return "".join(id)
```
**Purpose**: Generates unique 8-character account numbers  
**Format**: 3 letters + 3 digits + 2 special characters (shuffled)  
**Example Output**: `Z21)i*U9`

#### `Create_account()` - Instance Method
**Workflow**:
1. Collects user information (name, age, email, PIN)
2. Validates eligibility criteria
3. Generates unique account number
4. Initializes account with zero balance
5. Appends to in-memory data structure
6. Persists to database

**Validation Rules**:
- Age ≥ 18
- PIN must be exactly 4 digits

#### `deposit()` - Instance Method
**Workflow**:
1. Authenticates user with account number and PIN
2. Validates deposit amount
3. Updates account balance
4. Persists changes to database

**Business Rules**:
- Maximum single deposit: ₹100,000
- Minimum deposit: > ₹0

## 🛠️ Technologies & Libraries

| Library | Purpose |
|---------|---------|
| `json` | Data serialization and persistence |
| `random` | Random selection for account number generation |
| `string` | Character sets for ID generation |
| `pathlib.Path` | Cross-platform file path handling |

## 📊 Data Structure

### Account Object Schema
```json
{
    "name": "string",
    "age": "integer",
    "email": "string",
    "pin": "integer (4 digits)",
    "accountNo": "string (8 characters)",
    "balance": "float"
}
```

### Database Storage
- **File**: `data.json`
- **Format**: JSON array of account objects
- **Encoding**: UTF-8
- **Indentation**: 4 spaces for readability

## 🚀 Usage

### Running the Application
```bash
python main.py
```

### Menu Options
```
Press 1 For Creating an account
Press 2 for Depositing the Money in the bank
Press 3 For Withdrawing the money
Press 4 for details
Press 5 for updating details
Press 6 for deleting your account
```

### Example Workflow

**Creating an Account:**
```
Tell your response :- 1
Tell your name:- Varun Kumar
Tell your age:- 25
Tell your email:- varun@example.com
Tell your 4 no pin:- 1234

Account created successfully.
Account Number: A7b@3k*2
Please note down your account number for future reference.
```

**Making a Deposit:**
```
Tell your response :- 2
Enter your account number:- A7b@3k*2
Enter your pin:- 1234
Enter the amount to be deposited:- 5000

Amount 5000.0 deposited successfully. New balance is 5000.0
```

## 🔐 Security Considerations

- PIN-based authentication
- Private methods for internal operations (name mangling)
- Input validation at multiple levels
- Age verification for account creation

## 🎓 Key Programming Concepts

### Object-Oriented Programming
- Encapsulation: Data and methods bundled in `Bank` class
- Abstraction: Private methods hide implementation details
- Class vs Instance methods: Strategic use of decorators

### Data Persistence
- File I/O operations
- JSON serialization/deserialization
- Exception handling for file operations

### Input Validation
- Type checking (int, float conversions)
- Range validation (age, amount limits)
- Length validation (PIN digits)

### List Comprehension
```python
userdata = [user for user in Bank.data if user['accountNo'] == acc_no and user['pin'] == pin]
```
Efficient filtering of account data based on credentials

## 📁 Project Structure
```
Bank Management/
├── main.py           # Main application file
├── data.json         # Database file (auto-generated)
└── README.md         # Project documentation
```

## 🐛 Error Handling

- File not found handling during initialization
- Invalid input type handling
- Authentication failure messages
- Amount validation feedback

## 🔮 Future Enhancements

- [ ] Withdrawal functionality
- [ ] Account details viewer
- [ ] Profile update mechanism
- [ ] Account deletion with confirmation
- [ ] Transaction history
- [ ] Password encryption
- [ ] Multiple user session management
- [ ] GUI implementation

## 👨‍💻 Development Notes

**Language**: Python 3.x  
**Paradigm**: Object-Oriented Programming  
**Data Storage**: JSON-based flat file database  
**Interface**: Command-line interface (CLI)

---

**Developed as a demonstration of core banking operations with Python OOP principles and file-based data persistence.**