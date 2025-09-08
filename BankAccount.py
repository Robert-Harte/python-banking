#   Base class for bank accounts

class BankAccount:
    def __init__ (self, id, account_name, account_number):
        self.id = id
        self.account_name = account_name
        self.sort_code = "000000"   #   Different sort codes for each type. Review if this needs to be here?
        self.account_number = account_number
        self.balance = 0.00
        self.status = True          #    True = enabled, False = disabled

    def __bool__(self):
        return self.status != 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.id >= self.id:
            raise StopIteration
        else:
            self.id += 1
            return self.id - 1
        
    def change_account(self, attribute, value):
        match attribute:
            case "account_name":
                self.account_name = value        
            case "status":
                if value is True or value is False:
                    self.status = value
                else:
                    print(f"Error - the passed value was not correct! {value}")
                    
    #Update the balance of the account
    def update_balance(self, amount, type):
        if isinstance(amount, float):
            if(type == "credit"):
                self.balance += amount
            else:
                print("Debit method")
                self.balance -= amount
        else:
            print("This is not a valid amount!")
            
#*********************************************************************************************           
#   Current account class

class CurrentAccount(BankAccount):
    def __init__ (self, id, customer_id, account_name, account_number):
        super().__init__(id, account_name, account_number)
        self.customer_id = customer_id
        self.sort_code = "070116"

#*********************************************************************************************
#   Savings account class

class SavingsAccount(BankAccount):
    interest_rate = 5.00
    
    def __init__ (self, id, customer_id, cur_acc_id, account_name, account_number):
        super().__init__(id, account_name, account_number)
        self.customer_id = customer_id
        self.cur_acc_id = cur_acc_id
        self.sort_code = "200000"                             #    True = enabled, False = disabled
        self.interest_rate = SavingsAccount.interest_rate   #   Interest rate of the account. 

