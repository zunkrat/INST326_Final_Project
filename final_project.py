from argparse import ArgumentParser
import sys
import re
import pandas as pd

class PayStubExtraction:
    patterns = {
        'Direct Deposit Date': r'Paid by DIRECT DEPOSIT on (\d{2}-\d{2}-\d{4})',
        'Employee Full Name': r'(\w+ \w+ \w+)  \n',
        'Current Earnings': r'Earnings\n-\nTaxes\n-\nDeductions\n=\nNet Pay\nCurrent\n\s+(\d+\.\d{2})',
        'Current Taxes': r'Earnings\n-\nTaxes\n-\nDeductions\n=\nNet Pay\nCurrent\n\s+\d+\.\d{2}\n\s+(\d+\.\d{2})',
        'Net Pay': r'Net Pay\nCurrent\n\s+\d+\.\d{2}\n\s+\d+\.\d{2}\n.+\n\s+(\d+\.\d{2})'
    }

    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            text_content = file.read()

        extracted_info = {key: re.search(pattern, text_content).group(1) for key, pattern in self.patterns.items() if re.search(pattern, text_content)}

        self.direct_deposit_date = extracted_info.get('Direct Deposit Date', '')
        self.employee_full_name = extracted_info.get('Employee Full Name', '')
        self.current_earnings = extracted_info.get('Current Earnings', '')
        self.current_taxes = extracted_info.get('Current Taxes', '')
        self.net_pay = extracted_info.get('Net Pay', '')

class IncomeAllocator:
    """Class for managing income allocation to checking and savings accounts.
    
    Attributes:
        total_income (float): Total income amount.
        checking_percent (float): Percentage of the total income allocated to the checking account.
        savings_percent (float): Percentage of the total income allocated to the savings account.
        bank_accounts (dict): Dictionary to store allocated amounts in checking and savings accounts.        
    """
    
    def __init__(self, pay_stub_info, checking_percent, savings_percent):
        """
        Initialize the IncomeAllocator object.

        Args:
            total_income (float): Total income amount.
            checking_percent (float): Percentage of the total income allocated to the checking account.
            savings_percent (float): Percentage of the total income allocated to the savings account.
            bank_accounts (dict): Dictionary to store allocated amounts in checking and savings accounts.
            
        Side effects:
            Create IncomeAllocator attributes.
        """
        
        self.bank_accounts = {}
        self.total_income = float(pay_stub_info.net_pay)
        self.checking_percent = checking_percent
        self.savings_percent = savings_percent

    def check_percentage(self):
        """Check if the percentage is valid
        
        Returns:
            float: allocating percentage to checking and savings account.
            
        Raise:
            ValueError: Percentage has to be within 0 to 1.
        """
        
        if 0 <= self.checking_percent <= 1 and 0 <= self.savings_percent <= 1:
            return self.checking_percent, self.savings_percent
        else:
            raise ValueError("Percentage has to be within 0 to 1")

    def calculator(self):
        """Calculate and allocate income to checking and savings accounts.
        
        Returns:
            dict: the deposit amount to checking and savings account.
        """
        
        self.check_percentage()
        money_to_checking = round((self.total_income * self.checking_percent), 2)
        money_to_savings = round((self.total_income * self.savings_percent), 2)

        self.bank_accounts["checking"] = money_to_checking if isinstance(money_to_checking, float) else float(money_to_checking)
        self.bank_accounts["savings"] = money_to_savings if isinstance(money_to_savings, float) else float(money_to_savings)

        return self.bank_accounts

def main():
    """Calculate the amount to deposit into checking and savings account using the percentage from users and income read from the paystub.
    
    Args:
        checking_percent: percentage set by the user to allocate income to checking account.
        savings_percent: percentage set by the user to allocate income to savings account.
        income (float): Total income amount obtained from the paystub. A default value obtained from the paystub using the get_income_from_paystub() function.
    
    Returns:
        dict: the deposit amount to checking and savings account.
    """
    
    args = parse_args(sys.argv[1:])
    pay_stub_info = PayStubExtraction(args.filepath)
    income_allocator = IncomeAllocator(pay_stub_info, args.checking_percent, args.savings_percent)
    deposit = income_allocator.calculator()
    return deposit

def parse_args(arglist):
    """ Parse command-line arguments.
    
    Expect three mandatory arguments:
        - filepath: path to the file.
        - checking_percent: percentage set by the user to allocate income to checking account.
        - savings_percent: percentage set by the user to allocate income to savings account.
    
    Args:
        arglist (list of str): arguments from the command line.
    
    Returns:
        namespace: the parsed arguments, as a namespace.
    """
    
    parser = ArgumentParser()
    parser.add_argument("filepath", type = str, help = "Path to the pay stub file", default="converted_pay_stub.txt")
    parser.add_argument("checking_percent", type = float, help = "Percentage for checking")
    parser.add_argument("savings_percent", type = float, help = "Percentage for savings")

    return parser.parse_args(arglist)

def dic_csv(dictionary):
    """Transforms the dictionary of the bank accounts into a csv file.
    
    Args:
        dictionary: bank account dictionary (checking account and savings account).
    
    Side effects:
        csv_file: bank csv file that contain checking account and savings account balance will be created.
    """
    
    df = pd.DataFrame([dictionary])
    df.to_csv('bank.csv', index = False)
    
if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    pay_stub_info = PayStubExtraction(args.filepath)
    income_allocator = IncomeAllocator(pay_stub_info, args.checking_percent, args.savings_percent)
    deposit = income_allocator.calculator()
    
    dic_csv(deposit)