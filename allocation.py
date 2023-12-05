import re

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

def extract_pay_stub_info(file_path): #Tulasi Venkat
    
    #assumes that the file is a text file
    with open(file_path, 'r') as file:
        text = file.read()
        
    date_paid_regex = r"Date Paid: (\d{2}/\d{2}/\d{4})"
    gross_pay_regex = r"Gross Pay: \$(\d+.\d{2})"
    deductions_regex = r"Total Deductions: \$(\d+.\d{2})"
    net_pay_regex = r"Net Pay: \$(\d+.\d{2})"

    date_paid = re.search(date_paid_regex, text)
    gross_pay = re.search(gross_pay_regex, text)
    deductions = re.search(deduction_regex, text)
    net_pay = re.search(net_pay_regex, text)

    pay_stub_data = {
        "date_paid": date_paid.group(1)
        "gross_pay": gross_pay.group(1)
        "deduction": deductions.group(1)
        "net_pay": net_pay.group(1)
    }

def user_allocation(): #Ojie
    
    while True:
        categories = frozenset(['Entertainment', 'Groceries', 'Housing', 'Utilities', 'Travel', 'Recreation', 'Transportation', 'Other'])    
        allocation_percentages = {}
    
        print("Available Categories:")
        for category in categories:
            print(category)
        
        allocate = input("Do you want to allocate money to any of the above categories? Enter 'yes': ")

        if allocate.lower() != 'yes':
            break
    
        print("You will enter a percentage for each category, the '%' symbol is not required.")
        for category in categories:
            while True:
                try:
                    percentage = input(f"Enter a percetage for {category}: ")
                    percentage = float(percentage.rstrip('%'))
            
                    if(0<= percentage <=100):
                        allocation_percentages[category] = (percentage)
                        break
                        
                    else:
                        print("Enter a valid number between 0 and 100.")
                except ValueError:
                    print("Invalid input. Enter a number between 0 and 100.")
    



return pay_stub_data

