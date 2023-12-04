import re

class IncomeAllocator:
    
    def __init__(self, total_income, checking_percent, savings_percent, bank_accounts):
        self.bank_accounts = bank_accounts
        self.total_income = total_income
        self.checking_percent = checking_percent
        self.savings_percent = savings_percent

    def calculator(self):
        money_to_checking = self.total_income * self.checking_percent
        money_to_savings = self.total_income * self.savings_percent

        if isinstance(money_to_checking, (int, float)):
            checking_balance = self.bank_accounts.get("checking", 0)
            checking_balance += money_to_checking
            self.bank_accounts["checking"] = checking_balance

        if isinstance(money_to_savings, (int, float)):
            savings_balance = self.bank_accounts.get("savings", 0)
            savings_balance += money_to_savings
            self.bank_accounts["savings"] = savings_balance

    def get_total_balance(self):
        total_checking_balance = self.bank_accounts.get("checking", 0)
        total_savings_balance = self.bank_accounts.get("savings", 0)

        for account, balance in self.bank_accounts.items():
            if account == "checking":
                total_checking_balance += balance
            elif account == "savings":
                total_savings_balance += balance

        return total_checking_balance, total_savings_balance

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
    
    categories = ['entertainment', 'groceries', 'other','travel']
    # Different categories
    
    allocation_percentages = {}
    # Allocation percentage for each category
    
    for category in categories:
        percentage = input(f"Enter a percetage for {category}")
        allocation_percentages[category] = float(percentage)
    
    return allocation_percentages

def calculate_total_percentage(allocation_percentages): #Ojie
    total_percentage = sum(allocation_percentages.values())
    return total_percentage


return pay_stub_data


