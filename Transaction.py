from enum import Enum

# Transactions class. Implemented some error checking on certain fields. Should perhaps do all fields???

class Transaction:
    def __init__ (self, id, account_id, amount, description, date, type):
        self.id = id
        self.account_id = account_id    # Bank account id
        self.amount = amount            # Should be a positive number (the type will determine if it is added or subtracted)
        self.description = description
        self.date = date
        self.type = type

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
