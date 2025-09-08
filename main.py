import random
import datetime

#Custom imports
from Customer import Customer
from BankAccount import CurrentAccount
from BankAccount import SavingsAccount
from Transaction import Transaction

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
    print("X. Return to main menu")
    option = input("Select option: ").lower()
    return option

# Creates a new customer object. Returns the new customer to caller.
def create_customer(id, customer_name):
    print("*****************************************")
    customer = Customer(id, customer_name)
    return customer

# Displays the list of customers
def view_customers(accounts):
    print("*****************************************")
    print("Customer Accounts list:")
    for key, value in accounts.items():
        print(f"Account Id: {key}. Account name: {value}")

# Create a current account. Linked by customer_id to the customer.
def create_current_account(account_id, customer_id, account_name, account_number):
    account = CurrentAccount(account_id, customer_id, account_name, account_number)
    return account

# Create a savings account. Linked by acocunt_id to a current account.
def create_savings_account(account_id, customer_id, cur_acc_id, account_name, account_number):
    account = SavingsAccount(account_id, customer_id, cur_acc_id, account_name, account_number)
    return account

# Displays the list of current accounts for a specific customer
def view_customer_current_accounts(customer_name, customer_id, current_accounts):
    print("*****************************************")
    print(f"{customer_name} current account list:")
    
    for id, val in current_accounts.items():
        if val.customer_id == customer_id:
            print("---------------")
            print(f"Account ID: {val.id}\r\nCustomer ID: {val.customer_id}\r\nAccount name: {val.account_name}\r\nSort code: {val.sort_code}\r\nAccount number: {val.account_number}\r\nBalance: £{val.balance:.2f}\r\nStatus: {'Enabled' if val.status == True else 'Disabled'}")
            
# Displays the list of current accounts for a specific customer
def view_customer_savings_accounts(customer_name, customer_id, savings_accounts):
    print("*****************")
    print(f"{customer_name} savings account list:")
    
    for id, val in savings_accounts.items():
        if val.customer_id == customer_id:
            print("---------------")
            print(f"Account ID: {val.id}\r\nCustomer ID: {val.customer_id}\r\nCurrent Account ID: {val.cur_acc_id}\r\nAccount name: {val.account_name}\r\nSort code: {val.sort_code}\r\nAccount number: {val.account_number}\r\nBalance: £{val.balance:.2f}\r\nStatus: {'Enabled' if val.status == True else 'Disabled'}")

# Updates the current account. Only fields available are account name and status
def update_current_account(current_account):
    field = input("Enter field to update. (N) Account name, (S) Status, (Q) Quit: ").lower()
    match field:
        case "n":
            new_name = input("Enter new account name: ")
            current_account.change_account(attribute="account_name", value=new_name)
            return current_account
        case "s":
            new_status = input(f"Do you want to {'disable' if current_account.status == True else 'enable'} your account (Y) = yes, (N) = no: ").lower()
            if new_status == "y":
                current_account.change_account(attribute="status", value=False if current_account.status == True else True)
                print(f"Account has been {'enabled' if current_account.status == True else 'disabled'}")
                return current_account
            else:
                pass
        case "q":
            pass    

# Add transactions to the system to increase or decrease the balance.
def update_balance(account, transactions):
    # Validate on fields. This also be enforced by the Class as well.
    try:
        amount = float(input("Enter the amount: "))
        description = input("Enter a description for the payment: ")
        type = input("Enter a type (C) for Credit, (D) for Debit: ").lower()
        if(type != 'c' and type != 'd'):
            print("Invalid transaction type!")
            return ("Error")
        typeValue = ("credit" if type == 'c' else "debit")
        date = datetime.datetime.now()
        date = date.strftime("%Y-%m-%d %H:%M:%S")
        tran_id = len(transactions) + 1
        transaction = Transaction(tran_id, account.id, amount, description, date, typeValue)
        transactions.update({tran_id: transaction})
        account.update_balance(amount=amount, type=typeValue)
        response = (account, transactions)
        return response
    except ValueError:
        print(f"The amount you have entered is not valid!")
        return

# Displays the list of transactions for a specific account
def view_transactions(account_id, transactions):
    print("*****************************************")
    print("Transactions list:")
    
    for key, val in transactions.items():
        if val.account_id == account_id:
            print("---------------")
            print(f"Transaction ID: {key}\r\nAccount ID: {val.account_id}\r\nAmount: £{val.amount}\r\nDescription: {val.description}\r\nDate: {val.date}\r\nType: {val.type}")

def main():
    is_running = True
    accounts = {}
    current_accounts = {}
    savings_accounts = {}
    transactions = {}

    print("Welcome to Robert's Banking App. Please select an option:")
    while is_running:
        option = display_main_options()

        match option:
            case "1":   # Create a new customer.
                # Calls the create_customer method. Customer_Id increments by 1 each time. The customer name is entered by the user.
                customer = create_customer(100000 + len(accounts), input("Enter customer's name: "))
                accounts.update({customer.id: customer.account_name})
                print(f"New account successfully setup. ID: {customer.id}; Account name: {customer.account_name}")
            case "2":   # View list of customers
                view_customers(accounts)
            case "3":   # Manage customer accounts
                # Test if the customer_id is valid / exists in the accounts set.
                try:
                    customer_id = int(input("Enter the Customer ID: "))
                    if accounts.get(customer_id):
                        # Customer exists, so now go into the customer accounts menu.
                        while True:
                            cust_option = display_customer_options()
                            match cust_option:
                                case "1":   # View list of bank accounts
                                    view_customer_current_accounts(accounts.get(customer_id), customer_id, current_accounts)
                                    view_customer_savings_accounts(accounts.get(customer_id), customer_id, savings_accounts)
                                case "2":   # Create new bank account account
                                    acc_type = input("Enter account type (C) Current Account, (S) Savings Account: ").lower()
                                    if acc_type == 'c':
                                        account_name = input("Enter Bank Account Name: ")
                                        new_account = create_current_account(500000 + len(current_accounts), customer_id, account_name, random.randint(10000000, 99999999))
                                        current_accounts.update({new_account.id: new_account})
                                    elif acc_type == 's':
                                        # Check for active current account.
                                        current_account = int(input("Enter current account ID: "))
                                        if current_account in current_accounts:
                                            for key, val in current_accounts.items():
                                                if key == current_account and val.status == True:
                                                    account_name = input("Enter Bank Account Name: ")
                                                    new_account = create_savings_account(900000 + len(savings_accounts), customer_id, current_account, account_name, random.randint(10000000, 99999999))
                                                    savings_accounts.update({new_account.id: new_account})
                                                else:
                                                    print("Account is not active. Cannot create savings account.")
                                        else:
                                            print("Customer does not have an active current account. Cannot create a savings account!")
                                    else:
                                        print("Invalid account type!")
                                case "3":   # Editing the account. Select account, then call the update_current_account() method.
                                    # Keep running until the person quits
                                    while True:                                    
                                        current_account = int(input("Enter account ID: "))
                                        if current_account in current_accounts:
                                            for key, val in current_accounts.items():
                                                if key == current_account:
                                                    current_accounts[key] = update_current_account(val)
                                            break
                                        else:
                                            print(f"Bank account ID: {current_account} does not exist!")
                                            break
                                case "4":   # Add transactions to a bank account
                                    # Keep running until the person quits
                                    while True:
                                        account_id = int(input("Enter account ID: "))
                                        if account_id in current_accounts:
                                            for key, val in current_accounts.items():
                                                if key == account_id:
                                                    if(val.status is True):
                                                        response = update_balance(val, transactions)
                                                        if response == "Error":
                                                            pass
                                                        else:
                                                            current_accounts[key] = response[0]
                                                            transactions = response[1]
                                                    else:
                                                        print("Account is not active. Cannot add transactions.")
                                            break
                                        elif account_id in savings_accounts:
                                            for key, val in savings_accounts.items():
                                                if key == account_id:
                                                    if(val.status is True):
                                                        response = update_balance(val, transactions)
                                                        if response == "Error":
                                                            pass
                                                        else:
                                                            savings_accounts[key] = response[0]
                                                            transactions = response[1]
                                                    else:
                                                        print("Account is not active. Cannot add transactions.")
                                            break
                                        else:
                                            print(f"Bank account ID: {current_account} does not exist!")
                                case "5":   # View list of transactions for a bank account
                                    account_id = int(input("Enter account ID: "))
                                    if account_id in current_accounts:
                                        for key, val in current_accounts.items():
                                                view_transactions(account_id, transactions)
                                    elif account_id in savings_accounts:
                                        for key, val in savings_accounts.items():
                                                view_transactions(account_id, transactions)
                                    else:
                                        print(f"Bank account ID: {current_account} does not exist!")
                                case "x":
                                    break
                                case _:
                                    print("Invalid option! Please select another option: ")
                    else:
                        print(f"Customer ID {customer_id} does not exist!")
                except ValueError:
                    print(f"Invalid value!")
            case "q":   # Quit the application
                break
            case _:
                print("Invalid option! Please select another option: ")

if __name__ == "__main__":
    main()