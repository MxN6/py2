class Account():
    def __init__(self):
        self.balance = 0
    def deposit(self, cash):
        self.balance += cash
    def withdraw(self, amount):
        if amount > self.balance: 
            print("Insufficient Funds")
        else: 
            self.balance -= amount
            print(self.balance)

n = list(map(int, input().split()))
Messi = Account()
Messi.deposit(n[0])
Messi.withdraw(n[1])