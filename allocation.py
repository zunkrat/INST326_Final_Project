categories = ['entertainment', 'groceries', 'other','travel']

def __init__ (self, total_income, checking_percent, savings_percent, bank_accounts):

    self.bank_accounts = bank_accounts
    self.total_income = total_income
    self.checking_percent = checking_percent
    self.savings_percent = savings_percent

def calculator(self): # Gwon and Christian

    money_to_checking = self.total_income * self.checking_percent

    # budgetings such as groceries, etc from checking account.
    
    money_to_savings = self.total_income * self.savings_percent

    # budgetings such as groceries, etc from checking account.

    if isinstance(money_to_checking, int):
        checking_balance = self.bank_accounts["checking"]
        checking_balance += money_to_checking
        self.bank_accounts["checking"] = checking_balance
    
    if isinstance(money_to_savings, int):
        savings_balance = self.bank_accounts["savings"]
        savings_balance += money_to_savings
        self.bank_accounts["savings"] = savings_balance