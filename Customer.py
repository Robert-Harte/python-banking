class Customer:
    def __init__ (self, id, account_name):
        self.id = id
        self.account_name = account_name

    def __iter__(self):
        return self

    def __next__(self):
        if self.id >= self.id:
            raise StopIteration
        else:
            self.id += 1
            return self.id - 1