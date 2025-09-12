import random
import datetime
import mysql.connector
from decimal import Decimal

#Custom imports
from Customer import Customer
from BankAccount import CurrentAccount
from BankAccount import SavingsAccount
from Transaction import Transaction

mydb = mysql.connector.connect(
  host="localhost",
  user="python",
  password="B0tt0ml1n3",
  database="BankingApp"
)

mycursor = mydb.cursor()

# Displays the main list of options. Also returns the option selected.
def display_main_options():
    print("*****************************************")
    print("1. Create new customer")
    print("2. View customer list")
    print("3. View customer details")
    print("Q. Quit")
    option = input("Select option: ").lower()
    return option

def display_customer_options():
    print("*****************************************")
    print("1. View list of bank accounts")
    print("2. Create new bank account")
    print("3. Edit exsting account details")
    print("4. Update account balance")
    print("5. View account transactions")
    print("6. Calculate interest")
    print("X. Return to main menu")
    option = input("Select option: ").lower()
    return option

# Creates a new customer object. Returns the new customer to caller.
def create_customer():
    customer_name = input("Enter customer's name: ")
    print("*****************************************")
    mycursor.execute("SELECT COUNT(*) FROM customers")
    num_records = 0
    for x in mycursor:
        num_records = x[0] + 1
    mycursor.execute("INSERT INTO customers (id, name) VALUES (%s,%s)", (num_records,customer_name))
    mydb.commit()
    print(f"New account successfully setup. Account ID: {num_records}; Account name: {customer_name}")

# Displays the list of customers
def view_customers():
    print("*****************************************")
    print("Customer Accounts list:")

    mycursor.execute("SELECT * FROM customers")
    for x in mycursor:
        print(f"Account ID: {x[0]}. Account name: {x[1]}")

# Check if customer exists
def check_cust_exists(id):
    mycursor.execute(f"SELECT * FROM customers WHERE ID = {id}")
    for x in mycursor:
        if x[0] > 0:
            return (x[0], x[1])
        else:
            print(f"This account does not exist!")
            return "error"

# Create a bank account. Linked by customer_id to the customer.
def create_bank_account(customer):
    acc_type = input("Enter account type (C) Current Account, (S) Savings Account: ").lower()
    if acc_type == 'c':
        account_name = input("Enter Bank Account Name: ")
        mycursor.execute("INSERT INTO current_accounts (account_id, customer_id, account_name, sort_code, account_number, balance, status) VALUES (%s,%s,%s,%s,%s,%s,%s)", (random.randint(10000, 19999), customer[0], account_name, "070116", random.randint(10000000, 99999999), 0.00, True))
        mydb.commit()
        print(f"New current account successfully setup!")
    elif acc_type == 's':
        # Check for active current account.
        has_results = False        
        current_account = int(input("Enter current account ID: "))
        mycursor.execute(f"SELECT * FROM current_accounts WHERE account_id = {current_account}")
        for x in mycursor:
            has_results = True
            if x[7] == 1:
                account_name = input("Enter Bank Account Name: ")
                mycursor.execute("INSERT INTO savings_accounts (account_id, customer_id, cur_acc_id, account_name, sort_code, account_number, balance, interest_rate, status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (random.randint(20000, 29999),customer[0], random.randint(1000, 9999), account_name, "070116", random.randint(10000000, 99999999), 0.00, 5.00, True))
                mydb.commit()
                print(f"New savings account successfully setup!")
            else:
                print("The current account is not active! Cannot create savings account!")
        if not has_results:
            print("The current account does not exist!. Cannot create a savings account!")
    else:
        print("Invalid account type!")

# Displays the list of bank accounts for a specific customer
def view_customer_accounts(customer):
    print("*****************************************")
    print(f"{customer[1]} current account list:")
    
    mycursor.execute(f"SELECT * FROM current_accounts WHERE customer_id = {customer[0]}")
    for x in mycursor:
        print("---------------")
        print(f"Account ID: {x[1]}\r\nCustomer ID: {x[2]}\r\nAccount name: {x[3]}\r\nSort code: {x[4]}\r\nAccount number: {x[5]}\r\nBalance: £{x[6]:.2f}\r\nStatus: {'Enabled' if x[7] == 1 else 'Disabled'}")
    
    print("*****************")
    print(f"{customer[1]} savings account list:")
    
    mycursor.execute(f"SELECT * FROM savings_accounts WHERE customer_id = {customer[0]}")
    for x in mycursor:
        print("---------------")
        print(f"Account ID: {x[1]}\r\nCustomer ID: {x[2]}\r\nCurrent Account ID: {x[3]}\r\nAccount name: {x[4]}\r\nSort code: {x[5]}\r\nAccount number: {x[6]}\r\nBalance: £{x[7]:.2f}\r\nStatus: {'Enabled' if x[9] == 1 else 'Disabled'}")

# Updates the current account. Only fields available are account name and status
def update_current_account(customer):
    has_results = False        
    current_account = int(input("Enter current account ID: "))
    mycursor.execute(f"SELECT * FROM current_accounts WHERE account_id = {current_account}")
    for x in mycursor:
        has_results = True
        field = input("Enter field to update. (N) Account name, (S) Status, (Q) Quit: ").lower()
        match field:
            case "n":
                new_name = input("Enter new account name: ")
                mycursor.execute(f"UPDATE current_accounts SET account_name = '{new_name}' WHERE account_id = {current_account}")
                mydb.commit()
                print("Account name successfully updated!")
                break
            case "s":
                new_status = input(f"Do you want to {'disable' if x[7] == True else 'enable'} your account (Y) = yes, (N) = no: ").lower()
                if new_status == "y":
                    mycursor.execute(f"UPDATE current_accounts SET status = {1 if x[7] == 0 else 0} WHERE account_id = {current_account}")
                    mydb.commit()
                    print(f"Account status successfully updated! Account is now {'enabled' if x[7] == 0 else 'disabled'}")
                    break
                else:
                    pass
            case "q":
                pass
    if not has_results:
        print("The current account does not exist!. Cannot create a savings account!")

# Add transactions to the system to increase or decrease the balance.
def update_cur_acc_balance():
    has_results = False
    
    try:
        account_id = int(input("Enter account ID: "))
        mycursor.execute(f"SELECT * FROM current_accounts WHERE account_id = {account_id}")
        # Current Accounts
        for x in mycursor:
            has_results = True
            new_balance = x[6]
            if x[7] == 1:
                amount = Decimal(input("Enter the amount: "))
                description = input("Enter a description for the payment: ")
                type = input("Enter a type (C) for Credit, (D) for Debit: ").lower()
                if type == 'c':
                   new_balance += amount
                elif type == 'd':
                    new_balance -= amount
                else:
                    print("Invalid transaction type!")
                    return ("Error")
                typeValue = ("credit" if type == 'c' else "debit")
                date = datetime.datetime.now()
                date = date.strftime("%Y-%m-%d %H:%M:%S")
                mycursor.execute("INSERT INTO transactions (account_id, amount, description, type) VALUES (%s,%s,%s,%s)", (account_id, amount, description, typeValue))
                mydb.commit()
                print("Successfully added transaction! Updating account balance.")
                mycursor.execute(f"UPDATE current_accounts SET balance = {new_balance} WHERE account_id = {account_id}")
                mydb.commit()
                print(f"Balance successfully updated! New balance is: £{new_balance}")
            else:
                print("Account has been disabled! No new transactions can be added.")
        if not has_results:
            print(f"Bank account ID: {account_id} does not exist!")
    except ValueError:
        print(f"The amount you have entered is not valid!")
    return

# Add transactions to the system to increase or decrease the balance.
def update_sav_acc_balance():
    has_results = False
    
    try:
        account_id = int(input("Enter account ID: "))
        mycursor.execute(f"SELECT * FROM savings_accounts WHERE account_id = {account_id}")
        for x in mycursor:
            new_balance = x[7]
            has_results = True
            if x[9] == 1:
                amount = Decimal(input("Enter the amount: "))
                description = input("Enter a description for the payment: ")
                type = input("Enter a type (C) for Credit, (D) for Debit: ").lower()
                if type == 'c':
                   new_balance += amount
                elif type == 'd':
                    new_balance -= amount
                else:
                    print("Invalid transaction type!")
                    return ("Error")
                typeValue = ("credit" if type == 'c' else "debit")
                date = datetime.datetime.now()
                date = date.strftime("%Y-%m-%d %H:%M:%S")
                mycursor.execute("INSERT INTO transactions (account_id, amount, description, type) VALUES (%s,%s,%s,%s)", (account_id, amount, description, typeValue))
                print("Successfully added transaction! Updating account balance.")
                mycursor.execute(f"UPDATE savings_accounts SET balance = {new_balance} WHERE account_id = {account_id}")
                mydb.commit()
                print(f"Balance successfully updated! New balance is: £{new_balance}")
        if not has_results:
            print(f"Bank account ID: {account_id} does not exist!")
    except ValueError:
        print(f"The amount you have entered is not valid!")
    return  

# Displays the list of transactions for a specific account
def view_transactions():
    account_id = int(input("Enter account ID: "))
    mycursor.execute(f"SELECT * FROM transactions WHERE account_id = {account_id}")
    print("*****************************************")
    print("Transactions list:")
    for x in mycursor:
        print("---------------")
        print(f"Transaction ID: {x[0]}\r\nAccount ID: {x[1]}\r\nAmount: £{x[2]}\r\nDescription: {x[3]}\r\nDate: {x[4]}\r\nType: {x[5]}")

# Interest calculator for savings accounts
def interest_calculator():
    try:
        has_results = False
        id = int(input("Enter savings account ID: "))
        duration = int(input("Enter number of years to calculate interest for: "))
        mycursor.execute(f"SELECT balance, interest_rate FROM savings_accounts WHERE account_id = {id}")
        for x in mycursor:
            principal = x[0]
            counter = 0
            while counter < duration:
                principal += (principal / 100) * x[1]
                print(f"The amount will be after {counter + 1} years: £{principal:.2f}")
                counter += 1
    except ValueError:
        print("Account ID or duration must be a number!")
          
def main():
    is_running = True
    savings_accounts = {}

    print("Welcome to Robert's Banking App. Please select an option:")
    while is_running:
        option = display_main_options()
        match option:
            case "1":   # Create a new customer.
                # Calls the create_customer method. Customer_Id increments by 1 each time. The customer name is entered by the user.
                create_customer()
            case "2":   # View list of customers
                view_customers()
            case "3":   # Manage customer accounts
                # Test if the customer_id is valid / exists in the database.
                try:
                    customer = ()
                    customer = check_cust_exists(int(input("Enter the Customer ID: ")))
                    if customer != "error":
                        # Customer exists, so now go into the customer accounts menu.
                        while True:
                            cust_option = display_customer_options()
                            match cust_option:
                                case "1":   # View list of bank accounts
                                    view_customer_accounts(customer)
                                case "2":   # Create new bank account account
                                    create_bank_account(customer)
                                case "3":   # Editing the account. Select account, then call the update_current_account() method.
                                    update_current_account(customer)
                                case "4":   # Add transactions to a bank account
                                    type = input("Enter which account type you wish to update (C) Current Account, (S) Savings Account: ").lower()
                                    if type == "c":
                                        update_cur_acc_balance()
                                    elif type == "s":
                                        update_sav_acc_balance()
                                    else:
                                        print("Invalid option! Test")
                                case "5":   # View list of transactions for a bank account
                                    view_transactions()
                                case "6":   # Interest calculator for savings account.
                                    interest_calculator()                                    
                                case "x":
                                    break
                                case _:
                                    print("Invalid option! Please select another option: ")
                except ValueError:
                    print(f"Invalid value!")
            case "q":   # Quit the application
                break
            case _:
                print("Invalid option! Please select another option: ")

if __name__ == "__main__":
    main()