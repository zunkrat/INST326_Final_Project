import re
from argparse import ArgumentParser
import sys

class IncomeAllocator:
    """Class for managing income allocation to checking and savings accounts.
    
    Attributes:
        total_income (float): Total income amount.
        checking_percent (float): Percentage of the total income allocated to the checking account.
        savings_percent (float): Percentage of the total income allocated to the savings account.
        bank_accounts (dict): Dictionary to store allocated amounts in checking and savings accounts.        
    """

    def __init__(self, total_income, checking_percent, savings_percent):
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

        bank_accounts = {}
        
        self.bank_accounts = bank_accounts
        self.total_income = total_income
        self.checking_percent = checking_percent
        self.savings_percent = savings_percent
    
    def check_percentage(self):
        
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
        
        money_to_checking = self.total_income * self.checking_percent
        money_to_savings = self.total_income * self.savings_percent

        self.bank_accounts["checking"] = money_to_checking if isinstance(money_to_checking, (float)) else float(money_to_checking)
        self.bank_accounts["savings"] = money_to_savings if isinstance(money_to_savings, (float)) else float(money_to_savings)

        return self.bank_accounts

def get_income_from_paystub():
    # Replace this function with Tulasi's function later.
    return 1500 # 1500 is just example income

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

    income_allocator = IncomeAllocator(args.income, args.checking_percent, args.savings_percent)
    deposit = income_allocator.calculator()

    return deposit

def parse_args(arglist):
    """ Parse command-line arguments.
    
    Expect three mandatory arguments:
        - checking_percent: percentage set by the user to allocate income to checking account.
        - savings_percent: percentage set by the user to allocate income to savings account.
        - income (float): Total income amount obtained from the paystub. A default value obtained from the paystub using the get_income_from_paystub() function.
    
    Args:
        arglist (list of str): arguments from the command line.
    
    Returns:
        namespace: the parsed arguments, as a namespace.
    """
        
    parser = ArgumentParser()
    parser.add_argument("checking_percent", type=float, help="Percentage for checking")
    parser.add_argument("savings_percent", type=float, help="Percentage for savings")
    parser.set_defaults(income = get_income_from_paystub())

    return parser.parse_args(arglist)
    
if __name__ == "__main__":
    deposit = main()
    print(deposit) # To see if the code is working. Delete this line later. If you want to test, copy just IncomeAllocator class to new python file and run it.

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
    deductions = re.search(deductions_regex, text)
    net_pay = re.search(net_pay_regex, text)

    pay_stub_data = {
        "date_paid": date_paid.group(1),
        "gross_pay": gross_pay.group(1),
        "deduction": deductions.group(1),
        "net_pay": net_pay.group(1)
    }

def user_allocation(): # Ojie
    """
    Display a list of available categories and prompt the user to allocate a percentage
    for each category. The user can choose to skip allocation for each category.
    The '%' symbol is not required when entering percentages.

    Returns:
        dict: A dictionary containing the allocated percentages for each category.
              The keys are category names, and the values are the corresponding percentages.
    """

    while True:
        categories = frozenset(['Entertainment', 'Groceries', 'Housing', 'Utilities', 'Travel', 'Recreation', 'Transportation', 'Other'])
        allocation_percentages = {}

        print("Available Categories:")
        print(", ".join(categories))  

        allocate = input("Do you want to allocate money to any of the above categories? Enter 'yes'(or anything else to exit): ")

        if allocate.lower() != 'yes':
            break

        print("You will enter a percentage for each category. The '%' symbol is not required.")
        total_percentage = 0

        while True:
            category = input("Enter the category you want to add to (or 'end' to finish): ").capitalize()

            if category.lower() == 'end':
                break

            if category in categories:
                while True:
                    try:
                        percentage = input(f"Enter a percentage for {category}: ")
                        percentage = float(percentage.rstrip('%'))

                        if 0 <= percentage <= 100:
                            if total_percentage + percentage > 100:
                                print(f"Total percentage will exceed 100%. Current total: {total_percentage}%")
                            else:
                                allocation_percentages[category] = percentage
                                total_percentage += percentage
                                break
                        else:
                            print("Enter a valid number between 0 and 100.")
                    except ValueError:
                        print("Invalid input. Enter a number between 0 and 100.")
            else:
                print("Invalid category. Please choose from the available categories.")

        if total_percentage == 100:
            print("Total percentage reached 100%. Allocation completed.")
            break

        print("Allocations:")
        for category, percentage in allocation_percentages.items():
            print(f"{category}: {percentage}%")

        confirm = input("Do you want to confirm these allocations? Enter 'yes' to confirm, anything else to re-enter: ")
        if confirm.lower() == 'yes':
            break

user_allocation()

    



return pay_stub_data

