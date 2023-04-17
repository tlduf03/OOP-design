from abc import ABC, abstractclassmethod

class Transaction(ABC):
    def __init__(self, customerId, tellerId):
        self._customerId = customerId
        self._tellerId = tellerId

    def get_customer_id(self):
        return self._customerId

    def get_teller_id(self):
        return self._tellerId
    
    @abstractclassmethod
    def get_transaction_description(self):
        pass

class Deposit(Transaction):
    def __init__(self, customerId, tellerId, amount):
        super().__init__(customerId, tellerId)
        self._amount = amount

    def get_transaction_description(self):
        return f"Teller {self.get_teller_id()} deposited {self._amount} to account {self.get_customer_id()}"

class Withdrawal(Transaction):
    def __init__(self, customerId, tellerId, amount):
        super().__init__(customerId, tellerId)
        self._amount = amount

    def get_transaction_description(self):
        return f"Teller {self.get_teller_id()} withdrew {self._amount} from account {self.get_customer_id()}"

class OpenAccount(Transaction):
    def __init__(self, customerId, tellerId):
        super().__init__(customerId, tellerId)

    def get_transaction_description(self):
        return f"Teller {self.get_teller_id()} opened an account for account ID: {self.get_customer_id()}"
    
class BankTeller:
    def __init__(self, id):
        self._id = id

    def get_id(self):
        return self._id

class BankAccount:
    def __init__(self, name, Id, balance):
        self._name = name
        self._Id = Id
        self._balance = balance
    
    def get_balance(self):
        return self._balance
    
    def deposit(self, amount):
        self._balance += amount
    
    def withdraw(self, amount):
        self._balance -= amount

class BankSystem:
    def __init__(self, transactions, accounts):
        self._transactions = transactions #list of transaction logs
        self._accounts = accounts #list of BankAccount objects

    def get_account(self, customerId):
        return self._accounts[customerId]
    
    def get_accounts(self):
        return self._accounts
    
    def get_transactions(self):
        return self._transactions
    
    #1 Open account
    def open_account(self, customer_name, teller_id):
        #Create a new account
        customerId = len(self.get_accounts())
        account = BankAccount(customer_name, customerId, 0)
        self._accounts.append(account)

        #log the transaction
        transaction = OpenAccount(customerId, teller_id)
        self._transactions.append(transaction)
        return customerId
    
    #2 Deposit
    def deposit(self, customer_id, teller_id, amount):
        account = self.get_account(customer_id)
        account.deposit(amount)

        transaction = Deposit(customer_id, teller_id, amount)
        self._transactions.append(transaction)

    #3 Withdraw
    def withdraw(self, customer_id, teller_id, amount):
        account = self.get_account(customer_id)
        if account.get_balance() < amount:
            raise Exception("Insufficient balance!")
        account.withdraw(amount)

        transaction = Withdrawal(customer_id, teller_id, amount)
        self._transactions.append(transaction)


import random
class BankBranch:
    def __init__(self, address, cash_on_hand, bank_system):
        self._address = address
        self._cash_on_hand = cash_on_hand #availabe cash in a branch
        self._bank_system = bank_system #BankSystem object
        self._tellers = []
    
    def add_teller(self, teller):
        self._tellers.append(teller)

    def _get_available_teller(self):
        idx = random.randint(0,len(self._tellers)-1)
        return self._tellers[idx].get_id()

    def open_account(self, customer_name):
        if not self._tellers:
            raise ValueError("Branch does not have any teller")
        teller_id = self._get_available_teller()
        return self._bank_system.open_account(customer_name, teller_id)

    def deposit(self, customer_id, amount):
        if not self._tellers:
            raise ValueError("Branch does not have any teller")
        teller_id = self._get_available_teller()
        self._bank_system.deposit(customer_id, teller_id, amount)

    def withdraw(self, customer_id, amount):
        if self._cash_on_hand < amount:
            raise ValueError("Branch does not have enough cash")
        if not self._tellers:
            raise ValueError("Branch does not have any teller")
        teller_id = self._get_available_teller()
        self._cash_on_hand -= amount
        self._bank_system.withdraw(customer_id, teller_id, amount)

    def collect_cash(self, ratio):
        # Cash collected from Main bank
        cash_to_collect = round(self._cash_on_hand * ratio)
        self._cash_on_hand -= cash_to_collect
        return cash_to_collect

    def provide_cash(self, amount):
        self._cash_on_hand += amount

class Bank:
    def __init__(self, branches, bank_system, total_cash):
        self._branches = branches
        self._bank_system = bank_system
        self._total_cash = total_cash
    
    def add_branch(self, address, initial_funds):
        branch = BankBranch(address, initial_funds, self._bank_system)
        self._branches.append(branch)
        return branch
    
    def collect_cash(self, ratio):
        for branch in self._branches:
            self._total_cash += branch.collect_cash(ratio)

    def print_transactions(self):
        for transaction in self._bank_system.get_transactions():
            print(transaction.get_transaction_description())
    
bankSystem = BankSystem([], [])
bank = Bank([], bankSystem, 10000)

branch1 = bank.add_branch('123 Main St', 1000)
branch2 = bank.add_branch('456 Elm St', 1000)

branch1.add_teller(BankTeller(1))
branch1.add_teller(BankTeller(2))
branch2.add_teller(BankTeller(3))
branch2.add_teller(BankTeller(4))

customerId1 = branch1.open_account('John Doe')
customerId2 = branch1.open_account('Bob Smith')
customerId3 = branch2.open_account('Jane Doe')

branch1.deposit(customerId1, 100)
branch1.deposit(customerId2, 200)
branch2.deposit(customerId3, 300)

branch1.withdraw(customerId1, 50)
""" Possible Output:
    Teller 1 opened account 0
    Teller 2 opened account 1
    Teller 3 opened account 2
    Teller 1 deposited 100 to account 0
    Teller 2 deposited 200 to account 1
    Teller 4 deposited 300 to account 2
    Teller 2 withdrew 50 from account 0
"""

bank.print_transactions()