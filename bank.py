"""
Bank Management System - Refactored Bank Class

This module provides a Bank class with proper error handling, input validation,
password hashing, and complete banking operations.
"""

import json
import random
import string
import hashlib
import re
from pathlib import Path
from typing import Optional, Dict, List, Any


# Constants
MIN_AGE: int = 18
MAX_DEPOSIT: float = 100000.0
MIN_DEPOSIT: float = 0.01
PIN_LENGTH: int = 4
DATABASE_PATH: str = "data.json"


class BankError(Exception):
    """Base exception for Bank operations."""
    pass


class AccountNotFoundError(BankError):
    """Raised when an account is not found."""
    pass


class AuthenticationError(BankError):
    """Raised when authentication fails."""
    pass


class ValidationError(BankError):
    """Raised when input validation fails."""
    pass


class InsufficientFundsError(BankError):
    """Raised when there are insufficient funds for withdrawal."""
    pass


class Bank:
    """
    Bank class to handle banking operations.
    
    This class provides methods for account creation, deposits, withdrawals,
    account management, and data persistence using JSON storage.
    
    Attributes:
        database_path (str): Path to the JSON database file.
        data (List[Dict]): In-memory storage for account records.
    """
    
    database_path: str = DATABASE_PATH
    data: List[Dict[str, Any]] = []
    
    def __init__(self) -> None:
        """Initialize the Bank instance and load existing data."""
        self._load_database()
    
    def _load_database(self) -> None:
        """
        Load existing data from the database file.
        
        Raises:
            json.JSONDecodeError: If the database file contains invalid JSON.
        """
        try:
            if Path(Bank.database_path).exists():
                with open(Bank.database_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    if content.strip():
                        Bank.data = json.loads(content)
                    else:
                        Bank.data = []
            else:
                Bank.data = []
                self._update_database()
        except json.JSONDecodeError as e:
            print(f"Error loading database: Invalid JSON format - {e}")
            Bank.data = []
        except IOError as e:
            print(f"Error loading database: File I/O error - {e}")
            Bank.data = []
    
    @staticmethod
    def _update_database() -> None:
        """
        Persist the current data to the database file.
        
        Writes the current state of all accounts to the JSON database file.
        """
        try:
            with open(Bank.database_path, "w", encoding="utf-8") as file:
                file.write(json.dumps(Bank.data, indent=4))
        except IOError as e:
            print(f"Error saving database: {e}")
            raise BankError(f"Failed to save database: {e}")
    
    @classmethod
    def _account_number_generator(cls) -> str:
        """
        Generate a unique account number.
        
        Returns:
            str: A unique 8-character account number composed of
                 3 letters, 3 digits, and 2 special characters.
        """
        alpha = random.choices(string.ascii_letters, k=3)
        digit = random.choices(string.digits, k=3)
        special_char = random.choices("!@#$%^&*()", k=2)
        account_id = alpha + digit + special_char
        random.shuffle(account_id)
        return "".join(account_id)
    
    @staticmethod
    def _hash_pin(pin: str) -> str:
        """
        Hash a PIN using SHA-256.
        
        Args:
            pin: The PIN to hash (as string).
            
        Returns:
            str: The SHA-256 hash of the PIN.
        """
        return hashlib.sha256(pin.encode()).hexdigest()
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format.
        
        Args:
            email: The email address to validate.
            
        Returns:
            bool: True if email format is valid, False otherwise.
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_pin(pin: str) -> bool:
        """
        Validate PIN format.
        
        Args:
            pin: The PIN to validate (as string).
            
        Returns:
            bool: True if PIN is exactly 4 digits, False otherwise.
        """
        return pin.isdigit() and len(pin) == PIN_LENGTH
    
    @staticmethod
    def validate_name(name: str) -> bool:
        """
        Validate name format.
        
        Args:
            name: The name to validate.
            
        Returns:
            bool: True if name is valid (non-empty, contains only letters and spaces).
        """
        return bool(name.strip()) and all(c.isalpha() or c.isspace() for c in name)
    
    @staticmethod
    def validate_age(age: int) -> bool:
        """
        Validate age for account eligibility.
        
        Args:
            age: The age to validate.
            
        Returns:
            bool: True if age is at least MIN_AGE, False otherwise.
        """
        return age >= MIN_AGE
    
    def _find_account(self, account_no: str) -> Optional[Dict[str, Any]]:
        """
        Find an account by account number.
        
        Args:
            account_no: The account number to search for.
            
        Returns:
            Optional[Dict]: The account data if found, None otherwise.
        """
        for account in Bank.data:
            if account['accountNo'] == account_no:
                return account
        return None
    
    def _authenticate(self, account_no: str, pin: str) -> Dict[str, Any]:
        """
        Authenticate a user with account number and PIN.
        
        Args:
            account_no: The account number.
            pin: The PIN (unhashed).
            
        Returns:
            Dict: The account data if authentication succeeds.
            
        Raises:
            AccountNotFoundError: If account is not found.
            AuthenticationError: If PIN is incorrect.
        """
        account = self._find_account(account_no)
        if account is None:
            raise AccountNotFoundError("Account not found.")
        
        hashed_pin = self._hash_pin(pin)
        if account['pin'] != hashed_pin:
            raise AuthenticationError("Invalid PIN.")
        
        return account
    
    def verify_credentials(self, account_no: str, pin: str) -> bool:
        """
        Verify user credentials without returning account data.
        
        Args:
            account_no: The account number.
            pin: The PIN (unhashed).
            
        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        try:
            self._authenticate(account_no, pin)
            return True
        except (AccountNotFoundError, AuthenticationError):
            return False
    
    def create_account(self, name: str, age: int, email: str, pin: str) -> Dict[str, Any]:
        """
        Create a new bank account.
        
        Args:
            name: Account holder's name.
            age: Account holder's age.
            email: Account holder's email address.
            pin: 4-digit PIN for the account.
            
        Returns:
            Dict: The created account information (excluding hashed PIN).
            
        Raises:
            ValidationError: If any input validation fails.
        """
        # Validate inputs
        if not self.validate_name(name):
            raise ValidationError("Invalid name. Name should contain only letters and spaces.")
        
        if not self.validate_age(age):
            raise ValidationError(f"Age must be at least {MIN_AGE} years.")
        
        if not self.validate_email(email):
            raise ValidationError("Invalid email format.")
        
        if not self.validate_pin(pin):
            raise ValidationError(f"PIN must be exactly {PIN_LENGTH} digits.")
        
        # Create account
        account_no = self._account_number_generator()
        hashed_pin = self._hash_pin(pin)
        
        account = {
            "name": name.strip(),
            "age": age,
            "email": email.strip().lower(),
            "pin": hashed_pin,
            "accountNo": account_no,
            "balance": 0.0
        }
        
        Bank.data.append(account)
        self._update_database()
        
        # Return account info without hashed PIN
        return {
            "name": account["name"],
            "age": account["age"],
            "email": account["email"],
            "accountNo": account["accountNo"],
            "balance": account["balance"]
        }
    
    def deposit(self, account_no: str, pin: str, amount: float) -> Dict[str, Any]:
        """
        Deposit money into an account.
        
        Args:
            account_no: The account number.
            pin: The account PIN.
            amount: The amount to deposit.
            
        Returns:
            Dict: Updated account information.
            
        Raises:
            AccountNotFoundError: If account is not found.
            AuthenticationError: If PIN is incorrect.
            ValidationError: If amount is invalid.
        """
        if amount < MIN_DEPOSIT:
            raise ValidationError(f"Minimum deposit amount is {MIN_DEPOSIT}.")
        
        if amount > MAX_DEPOSIT:
            raise ValidationError(f"Maximum deposit limit is {MAX_DEPOSIT}.")
        
        account = self._authenticate(account_no, pin)
        account['balance'] += amount
        self._update_database()
        
        return {
            "name": account["name"],
            "accountNo": account["accountNo"],
            "new_balance": account["balance"],
            "deposited": amount
        }
    
    def withdraw(self, account_no: str, pin: str, amount: float) -> Dict[str, Any]:
        """
        Withdraw money from an account.
        
        Args:
            account_no: The account number.
            pin: The account PIN.
            amount: The amount to withdraw.
            
        Returns:
            Dict: Updated account information.
            
        Raises:
            AccountNotFoundError: If account is not found.
            AuthenticationError: If PIN is incorrect.
            ValidationError: If amount is invalid.
            InsufficientFundsError: If balance is insufficient.
        """
        if amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        
        account = self._authenticate(account_no, pin)
        
        if account['balance'] < amount:
            raise InsufficientFundsError(
                f"Insufficient funds. Current balance: {account['balance']}"
            )
        
        account['balance'] -= amount
        self._update_database()
        
        return {
            "name": account["name"],
            "accountNo": account["accountNo"],
            "new_balance": account["balance"],
            "withdrawn": amount
        }
    
    def get_details(self, account_no: str, pin: str) -> Dict[str, Any]:
        """
        Get account details.
        
        Args:
            account_no: The account number.
            pin: The account PIN.
            
        Returns:
            Dict: Account details (PIN is masked).
            
        Raises:
            AccountNotFoundError: If account is not found.
            AuthenticationError: If PIN is incorrect.
        """
        account = self._authenticate(account_no, pin)
        
        return {
            "name": account["name"],
            "age": account["age"],
            "email": account["email"],
            "accountNo": account["accountNo"],
            "balance": account["balance"],
            "pin": "****"  # Masked PIN
        }
    
    def update_details(
        self, 
        account_no: str, 
        pin: str, 
        name: Optional[str] = None,
        email: Optional[str] = None,
        new_pin: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update account details.
        
        Args:
            account_no: The account number.
            pin: The current account PIN.
            name: New name (optional).
            email: New email (optional).
            new_pin: New PIN (optional).
            
        Returns:
            Dict: Updated account details.
            
        Raises:
            AccountNotFoundError: If account is not found.
            AuthenticationError: If PIN is incorrect.
            ValidationError: If new values are invalid.
        """
        account = self._authenticate(account_no, pin)
        
        if name is not None:
            if not self.validate_name(name):
                raise ValidationError("Invalid name. Name should contain only letters and spaces.")
            account['name'] = name.strip()
        
        if email is not None:
            if not self.validate_email(email):
                raise ValidationError("Invalid email format.")
            account['email'] = email.strip().lower()
        
        if new_pin is not None:
            if not self.validate_pin(new_pin):
                raise ValidationError(f"PIN must be exactly {PIN_LENGTH} digits.")
            account['pin'] = self._hash_pin(new_pin)
        
        self._update_database()
        
        return {
            "name": account["name"],
            "age": account["age"],
            "email": account["email"],
            "accountNo": account["accountNo"],
            "balance": account["balance"],
            "message": "Account updated successfully."
        }
    
    def delete_account(self, account_no: str, pin: str) -> Dict[str, str]:
        """
        Delete an account.
        
        Args:
            account_no: The account number.
            pin: The account PIN.
            
        Returns:
            Dict: Confirmation message.
            
        Raises:
            AccountNotFoundError: If account is not found.
            AuthenticationError: If PIN is incorrect.
        """
        account = self._authenticate(account_no, pin)
        
        Bank.data.remove(account)
        self._update_database()
        
        return {
            "message": f"Account {account_no} has been deleted successfully."
        }
    
    def account_exists(self, account_no: str) -> bool:
        """
        Check if an account exists.
        
        Args:
            account_no: The account number to check.
            
        Returns:
            bool: True if account exists, False otherwise.
        """
        return self._find_account(account_no) is not None


# CLI interface for backward compatibility
def main() -> None:
    """Command-line interface for the Bank Management System."""
    bank = Bank()
    
    print("\n" + "=" * 50)
    print("       BANK MANAGEMENT SYSTEM")
    print("=" * 50)
    print("Press 1 For Creating an account")
    print("Press 2 for Depositing the Money in the bank")
    print("Press 3 For Withdrawing the money")
    print("Press 4 for details")
    print("Press 5 for updating details")
    print("Press 6 for deleting your account")
    print("=" * 50)
    
    try:
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            print("\n--- Create Account ---")
            name = input("Enter your name: ")
            age = int(input("Enter your age: "))
            email = input("Enter your email: ")
            pin = input("Enter a 4-digit PIN: ")
            
            result = bank.create_account(name, age, email, pin)
            print("\n✓ Account created successfully!")
            print(f"Account Number: {result['accountNo']}")
            print("Please note down your account number for future reference.")
            
        elif choice == "2":
            print("\n--- Deposit Money ---")
            account_no = input("Enter your account number: ")
            pin = input("Enter your PIN: ")
            amount = float(input("Enter amount to deposit: "))
            
            result = bank.deposit(account_no, pin, amount)
            print(f"\n✓ Deposited: ₹{result['deposited']}")
            print(f"New Balance: ₹{result['new_balance']}")
            
        elif choice == "3":
            print("\n--- Withdraw Money ---")
            account_no = input("Enter your account number: ")
            pin = input("Enter your PIN: ")
            amount = float(input("Enter amount to withdraw: "))
            
            result = bank.withdraw(account_no, pin, amount)
            print(f"\n✓ Withdrawn: ₹{result['withdrawn']}")
            print(f"New Balance: ₹{result['new_balance']}")
            
        elif choice == "4":
            print("\n--- Account Details ---")
            account_no = input("Enter your account number: ")
            pin = input("Enter your PIN: ")
            
            result = bank.get_details(account_no, pin)
            print("\n" + "-" * 30)
            for key, value in result.items():
                print(f"{key.title()}: {value}")
            print("-" * 30)
            
        elif choice == "5":
            print("\n--- Update Details ---")
            account_no = input("Enter your account number: ")
            pin = input("Enter your PIN: ")
            
            print("\nWhat would you like to update?")
            print("1. Name")
            print("2. Email")
            print("3. PIN")
            update_choice = input("Enter choice (or press Enter to skip): ").strip()
            
            name = None
            email = None
            new_pin = None
            
            if update_choice == "1":
                name = input("Enter new name: ")
            elif update_choice == "2":
                email = input("Enter new email: ")
            elif update_choice == "3":
                new_pin = input("Enter new 4-digit PIN: ")
            
            result = bank.update_details(account_no, pin, name, email, new_pin)
            print(f"\n✓ {result['message']}")
            
        elif choice == "6":
            print("\n--- Delete Account ---")
            account_no = input("Enter your account number: ")
            pin = input("Enter your PIN: ")
            
            confirm = input("Are you sure you want to delete your account? (yes/no): ")
            if confirm.lower() == "yes":
                result = bank.delete_account(account_no, pin)
                print(f"\n✓ {result['message']}")
            else:
                print("\nAccount deletion cancelled.")
        
        else:
            print("\nInvalid choice. Please try again.")
            
    except ValidationError as e:
        print(f"\n✗ Validation Error: {e}")
    except AccountNotFoundError as e:
        print(f"\n✗ {e}")
    except AuthenticationError as e:
        print(f"\n✗ {e}")
    except InsufficientFundsError as e:
        print(f"\n✗ {e}")
    except ValueError as e:
        print(f"\n✗ Invalid input: Please enter valid numbers.")
    except BankError as e:
        print(f"\n✗ Error: {e}")


if __name__ == "__main__":
    main()
