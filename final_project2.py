from argparse import ArgumentParser
import sys
import re
import pandas as pd

class PayStubExtraction:
    """Class that extracts specific information from an uploaded paystub.
    
    Attributes:
        direct_deposit_date (str): the date on which the payment was made
        employee_full_name (str): the full name of the employee
        current_earnings (str): the current earnings from the payment period
        current_taxes (str): the amount of current taxes from the payment period
        net_pay (str): the total amount the employee is paid
    """
    def __init__(self, direct_deposit_date, employee_full_name, current_earnings, current_taxes, net_pay):
        """Initializes PayStubExtraction with the attributes.
        
        Args:
            direct_deposit_date (str): the date on which the payment was made
            employee_full_name (str): the full name of the employee
            current_earnings (str): the current earnings from the payment period
            current_taxes (str): the amount of current taxes from the payment period
            net_pay (str): the total amount the employee is paid
        """
        self.direct_deposit_date = direct_deposit_date
        self.employee_full_name = employee_full_name
        self.current_earnings = current_earnings
        self.current_taxes = current_taxes
        self.net_pay = net_pay
        
    patterns = {
        'Direct Deposit Date': r'Paid by DIRECT DEPOSIT on (\d{2}-\d{2}-\d{4})',
        'Employee Full Name': r'^(?:[^\n]*\n){2}([^\n]+)',
        'Current Earnings': r'CURRENT\s*[\s\S]*?(\d+,\d+\.\d{2})',
        'Current Taxes': r'TAXES/DEDUCTIONS\s*[\s\S]*?CURRENT\s*[\s\S]*?(\d+\.\d{2})',
        'Net Pay': r'Net Pay\s*[\s\S]*?(\d+,\d+\.\d{2})'
    }

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

        if 0 <= checking_percent <= 1 and 0 <= savings_percent <= 1:
            self.checking_percent = checking_percent
            self.savings_percent = savings_percent
        else:
            raise ValueError("Percentage has to be within 0 to 1")

    def check_percentage(self):
        """Check if the percentage is added up to 1
        
        Raises:
            ValueError: Percentage has to be within 0 to 1.
        """
        if self.checking_percent + self.savings_percent == 1:
            self.checking_percent = self.checking_percent
            self.savings_percent = self.savings_percent
        else:
            raise ValueError("Checking percent and savings percent must equal to 1")

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
    
    def user_allocation(self):
        """
        Display a list of available categories and prompt the user to allocate a percentage
        for each category. 

        Returns:
            dict: A dictionary containing the allocated percentages for each category.
                  The keys are category names, and the values are the corresponding percentages.
        """
        categories = frozenset(['Entertainment', 'Groceries', 'Housing', 'Utilities', 'Travel', 'Recreation', 'Transportation', 'Other'])
        allocation_percentages = {}

        print("Available Categories:")
        print(", ".join(categories))

        allocate = input("Do you want to allocate money to any of the above categories? Enter 'yes' (or anything else to exit): ")

        if allocate.lower() == 'yes':
            checking_amount = round((self.total_income * self.checking_percent), 2)
            print(f"Total amount available in checking based on checking percent ({self.checking_percent * 100}%): {checking_amount}")
            print("You will enter a percentage for each category. The '%' symbol is not required.")
            total_percentage = 0

            while total_percentage < self.checking_percent * 100:
                category = input("Enter the category you want to add to (or 'end' to finish): ").capitalize()

                if category.lower() == 'end':
                    break

                if category in categories:
                    remaining_percentage = self.checking_percent * 100 - total_percentage
                    print(f"Remaining percentage: {remaining_percentage}%")
                    percentage = self.get_percentage_input(f"Enter a percentage for {category}: ")

                    if total_percentage + percentage > self.checking_percent * 100:
                        print(f"Total percentage will exceed the checking percent ({self.checking_percent * 100}%). Current total: {total_percentage}%")
                    else:
                        allocation_percentages[category] = percentage
                        total_percentage += percentage
                else:
                    print("Invalid category. Please choose from the available categories.")


            print("Allocations:")
            for category, percentage in allocation_percentages.items():
                allocated_amount = round(((percentage / 100) * checking_amount), 2)
                print(f"{category}: {percentage}% - Allocated Amount: {allocated_amount}")

        return allocation_percentages
    
    def get_percentage_input(self, prompt):
        """
        Helper function to get a valid percentage input from the user.

        Args:
            prompt (str): The prompt to display.

        Returns:
            float: The valid percentage entered by the user.
        """
        while True:
            try:
                percentage = input(prompt)
                percentage = float(percentage.rstrip('%'))

                if 0 <= percentage <= 100:
                    return percentage
                else:
                    print("Enter a valid number between 0 and 100.")
            except ValueError:
                print("Invalid input. Enter a number between 0 and 100.")

def main():
    """Calculate the amount to deposit into checking and savings account using the percentage from users and income read from the paystub.
    
    Args:
        checking_percent: percentage set by the user to allocate income to checking account.
        savings_percent: percentage set by the user to allocate income to savings account.
        income (float): Total income amount obtained from the paystub. A default value obtained from the paystub using the get_income_from_paystub() function.
    
    Returns:
        dict: the deposit amount to checking and savings account.
    """
    
    if len(sys.argv) > 1:
        args = parse_args(sys.argv[1:])
        filepath = args.filepath
        checking_percent = args.checking_percent
        savings_percent = args.savings_percent
    else:
        # Gets user inputs 
        filepath = input("Enter the path to your paystub file: ")
        checking_percent = float(input("Enter the percentage to allocate to the checking account (0-100): ")) / 100
        savings_percent = float(input("Enter the percentage to allocate to the savings account (0-100): ")) / 100

        # Validates the input percentages
        if not 0 <= checking_percent <= 1 or not 0 <= savings_percent <= 1:
            raise ValueError("Percentages must be between 0 and 100")
        
    #Processes the pay stub    
    with open(filepath, 'r') as file:
        text_content = file.read()
    extracted_info = {key: re.search(pattern, text_content).group(1) for key, pattern in PayStubExtraction.patterns.items() if re.search(pattern, text_content)}
    
    #Gets rid of commas in the numbers as strings
    extracted_info['Current Earnings'] = extracted_info['Current Earnings'].replace(',', '')
    extracted_info['Current Taxes'] = extracted_info['Current Taxes'].replace(',', '')
    extracted_info['Net Pay'] = extracted_info['Net Pay'].replace(',', '')
         
    #Creates the PayStubExtraction object
    pay_stub_info = PayStubExtraction(
        direct_deposit_date = extracted_info['Direct Deposit Date'],
        employee_full_name = extracted_info['Employee Full Name'],
        current_earnings = extracted_info['Current Earnings'],
        current_taxes = extracted_info['Current Taxes'],
        net_pay = extracted_info['Net Pay']
    )
    
    income_allocator = IncomeAllocator(pay_stub_info, checking_percent, savings_percent)
    deposit = income_allocator.calculator()
    deposit['deposit date'] = pay_stub_info.direct_deposit_date
    
    print(f"Allocated amounts: {deposit}")
    income_allocator.user_allocation()

    dic_csv(deposit)
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
    """Appends the dictionary of the bank accounts to a CSV file.

    Args:
        dictionary: bank account dictionary (checking account and savings account).

    Side effects:
        csv_file: bank csv file that contains checking account and savings account balances will be created or appended.
    """
    df = pd.DataFrame([dictionary])

    csv_file_path = 'bank.csv'

    try:
        with open(csv_file_path, 'a', newline = '') as file:
            df.to_csv(file, index = False)
            
    except:
        with open(csv_file_path, 'w', newline = '') as file:
            df.to_csv(file, index = False)

if __name__ == "__main__":
    main()
