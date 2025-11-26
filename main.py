import json
import random
import string
from pathlib import Path


class Bank:                                       # Bank class to handle banking operations
    database_path = "data.json"                   # Path to the database file
    data = []                                     # List to hold account info
    
    
    try:                                          # Load existing info from the database file if it exists(try block)
        if Path(database_path).exists():          # Check if the database file exists
            with open(database_path, "r") as file: # Open the database file in read mode
                data = json.loads(file.read())        # Load the info from the file into the data list
        else:
            print(f"Database file not found at {database_path}, creating a new one.")
    except:                                       # Handle exceptions that may occur during file operations
        print(f"An exception occurred while loading the database file {database_path}")
        
        
    @staticmethod
    def __update_database():
        with open(Bank.database_path, "w") as file:
            file.write(json.dumps(Bank.data, indent=4))
            
    @classmethod
    def __account_number_generator(cls):
        alpha = random.choices(string.ascii_letters, k=3)
        digit = random.choices(string.digits, k=3)
        special_char = random.choices("!@#$%^&*()", k=2)
        id = alpha + digit + special_char
        random.shuffle(id)
        return "".join(id)
    
    
    
    
    def Create_account(self):
        info = {
            "name": input("Tell your name:- "),
            "age": int(input("Tell your age:- ")),
            "email": input("Tell your email:-"),
            "pin": int(input("Tell your 4 no pin:- ")),
            "accountNo": Bank.__account_number_generator(),
            "balance": 0
            }
        
        if info['age'] < 18 or len(str(info['pin'])) != 4:
            print("Sorry, yor are not eligible to create an account.")
        else:
            print("Account- created successfully.")
            for i in info:
                print(f"{i}: {info[i]}")
            print("Please note down your account number for future reference.")
            Bank.data.append(info)
            
            Bank.__update_database()
            
    def deposit(self):
        acc_no = input("Enter your account number:- ")
        pin = int(input("Enter your your pin:- "))
        
        userdata = [user for user in Bank.data if user['accountNo'] == acc_no and user['pin'] == pin]     # Fetch user data matching account number and pin
        
        if userdata == False:
            print("Invalid account number or pin.")
        else:
            amount = float(input("Enter the amount to be deposited:- "))
            if amount > 100000 or amount <= 0:
                print("Invalid amount.")
            else:
                userdata['balance'] += amount
                print(f"Amount {amount} deposited successfully. New balance is {userdata['balance']}.")
                Bank.__update_database()
        
                



user = Bank()
print("Press 1 For Creating an account")
print("Press 2 for Depositing the Money in the bank")
print("Press 3 For Withdrawing the money")
print("Press 4 for details")
print("Press 5 for updating details")
print("Press 6 for deleting your account")


check = int(input("Tell your response :-"))

if check == 1:
    user.Create_account()

if check == 2:
    user.deposit()