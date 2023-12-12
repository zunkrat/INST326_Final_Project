from argparse import ArgumentParser
import sys
import re
import pandas as pd
import matplotlib.pyplot as plt

class PayStubExtraction:
    """Class that extracts specific information from an uploaded paystub.
    
    Attributes:
        direct_deposit_date (str): the date on which the payment was made
        employee_full_name (str): the full name of the employee
        current_earnings (str): the current earnings from the payment period
        current_taxes (str): the amount of current taxes from the payment period
        net_pay (str): the total amount the employee is paid

    Primary Author of Class: Tulasi Venkat
    """
    def __init__(self, direct_deposit_date, employee_full_name, current_earnings, current_taxes, net_pay):
        """Initializes PayStubExtraction with the attributes.
        
        Args:
            direct_deposit_date (str): the date on which the payment was made
            employee_full_name (str): the full name of the employee
            current_earnings (str): the current earnings from the payment period
            current_taxes (str): the amount o11_4f current taxes from the payment period
            net_pay (str): the total amount the employee is paid
        """
        self.direct_deposit_date = direct_deposit_date
        self.employee_full_name = employee_full_name
        self.current_earnings = current_earnings
        self.current_taxes = current_taxes
        self.net_pay = net_pay
    
    def extract_paystub_info(self, paystub_text):
        """Extracts direct deposit date, employee name, current earnings, current taxes, 
        and net pay from the paystub text. It uses regular expressions to identify and extract that 
        information and creates a dictionary with the previously mentioned data.
        
        Args: 
            paystub_text (str): A string that contains the text from the paystub
        
        Returns:
            dict: Dictionary with the keys 'Direct Deposit Date', 'Employee Full Name', 'Current Earnings', 
                'Current Taxes', and 'Net Pay', which are mapped to their corresponding extracted value from the paystub.
        
        Primary Author of Method: Tulasi Venkat
        Technique: Regular Expressions
        """
        patterns = {
            'Direct Deposit Date': r'Paid by DIRECT DEPOSIT on (\d{2}-\d{2}-\d{4})',
            'Employee Full Name': r'^(?:[^\n]*\n){2}([^\n]+)',
            'Current Earnings': r'CURRENT\s*[\s\S]*?(\d+,\d+\.\d{2})',
            'Current Taxes': r'TAXES/DEDUCTIONS\s*[\s\S]*?CURRENT\s*[\s\S]*?(\d+\.\d{2})',
            'Net Pay': r'Net Pay\s*[\s\S]*?(\d+,\d+\.\d{2})'
        }
        extracted_info = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, paystub_text)
            extracted_info[key] = match.group(1) if match else None
            
        return extracted_info
    
    def extract_from_file(self, filepath):
        """Reads in a paystub file and extracts the key information. It opens the filepath containing the paystub,
        reads in the content, and calls the extract_paystub_info method to extract the data.
        
        Args:
            filepath (str): the path to the file containing the paystub
            
        Returns: 
            dict: Dictionary with the keys 'Direct Deposit Date', 'Employee Full Name', 'Current Earnings', 
                'Current Taxes', and 'Net Pay', which are mapped to their corresponding extracted value from the paystub.
       
        Primary Author of Method: Tulasi Venkat
        Technique: with statement
        """
        with open(filepath, 'r') as file:
            text_content = file.read()
            
        return self.extract_paystub_info(text_content)
    
    

class IncomeAllocator:
    """Class for managing income allocation to checking and savings accounts.
    
    Attributes:
        pay_stub_info (dict): Paystub information.
        checking_percent (float): Percentage of the total income allocated to the checking account.
        savings_percent (float): Percentage of the total income allocated to the savings account.
        bank_accounts (dict): Dictionary to store allocated amounts in checking and savings accounts.        
    """
    
    def __init__(self, pay_stub_info, checking_percent, savings_percent):
        """Initialize the IncomeAllocator object.

        Args:
            pay_stub_info (dict): Paystub information.
            checking_percent (float): Percentage of the total income allocated to the checking account.
            savings_percent (float): Percentage of the total income allocated to the savings account.
            
        Side effects:
            Create IncomeAllocator attributes.
            
        Primary Author of Method: Gwon Lee
        """
        
        self.bank_accounts = {}
        self.total_income = float(pay_stub_info.net_pay.replace(',', ''))

        if 0 <= checking_percent <= 1 and 0 <= savings_percent <= 1:
            self.checking_percent = checking_percent
            self.savings_percent = savings_percent
        else:
            raise ValueError("Percentage has to be within 0 to 1")

    def check_percentage(self):
        """Check if the percentage is added up to 1
        
        Raises:
            ValueError: Percentage has to be within 0 to 1.
        
        Primary Author of Method: Gwon Lee
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

        Primary Author of Method: Gwon Lee
        Technique: Conditional Expressions
        """
        
        self.check_percentage()
        money_to_checking = round((self.total_income * self.checking_percent), 2)
        money_to_savings = round((self.total_income * self.savings_percent), 2)

        self.bank_accounts["checking"] = money_to_checking if isinstance(money_to_checking, float) else float(money_to_checking)
        self.bank_accounts["savings"] = money_to_savings if isinstance(money_to_savings, float) else float(money_to_savings)

        return self.bank_accounts
    
    def __str__(self):
        
        '''
        To represent an informal string representation of the total income, checkings percent, savings percent, and
        bank Accounts
        
        Primary Author of Magic Method : Andy Do
        
        '''
        
        return (
            f'Total Income: {self.total_income}' '\n'
            f'Checking Percent: {self.checking_percent}' '\n'
            f'Savings Percent: {self.savings_percent}' '\n'
            f'Bank Accounts: {self.bank_accounts}'
        )
    
    def user_allocation(self):
        """
        Display a list of available categories and prompt the user to allocate a percentage
        for each category. 

        Returns:
            dict: A dictionary containing the allocated percentages for each category.
                  The keys are category names, and the values are the corresponding percentages.
                  
        Primary author of method: Ojie Okodogbe
        Technique: Operations on frozen sets
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
            
        Primary author of method: Ojie Okodogbe
        Technique: Keyword arguments
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

    Primary Author of Method: Gwon Lee
    Technique: The ArgumentParser class from the argparse module
    """
    
    parser = ArgumentParser()
    parser.add_argument("filepath", type = str, help = "Path to the pay stub file", default="converted_pay_stub.txt")
    parser.add_argument("checking_percent", type = float, help = "Percentage for checking")
    parser.add_argument("savings_percent", type = float, help = "Percentage for savings")

    return parser.parse_args(arglist)

def dic_csv(dictionary):
    """
    Appends the dictionary of the bank accounts to a CSV file.

    Args:
        dictionary: bank account dictionary (checking account and savings account).

    Side effects:
        csv_file: bank csv file that contains checking account and savings account balances will be created or appended.
        
    Primary Author for function: Andy Do
    
    """
    df = pd.DataFrame([dictionary])

    csv_file_path = 'bank.csv'

    try:
        with open(csv_file_path, 'r', newline = '') as file:
            existing_data = file.read()

        if not existing_data:
            df.to_csv(csv_file_path, index = False)
            
        else:
            with open(csv_file_path, 'a', newline = '') as file:
                df.to_csv(file, index = False, header = False)

    except Exception as e:
        print(f"Error writing to CSV file: {e}")
        

                
def recent_income(csv_file = 'bank.csv', num_rows = 10):
    """
    Plot the sum of checking and savings for the specified number of most recent paystubs from a CSV file.

    Args:
        csv_file (str): Path to the CSV file containing paystub data.
        num_rows (int): Number of most recent paystubs to include in the plot.

    Returns:
        None


    By Christian Bechmann - visualizing data with pyplot or seaborn
    """
    try:
        df = pd.read_csv(csv_file)
        
    except FileNotFoundError:
        print(f"File {csv_file} not found. Creating a new file. Please try it again.")
        df = pd.DataFrame(columns = ['checking', 'savings', 'deposit date'])
        df.to_csv(csv_file, index = False)

    df['Net Pay'] = df['checking'] + df['savings']
    
    selected_columns = ['deposit date', 'Net Pay']
    df = df[selected_columns]
    df['deposit date'] = pd.to_datetime(df['deposit date'], format = '%m-%d-%Y')
    df = df.sort_values(by = 'deposit date', ascending = False)
    recent_rows = df.head(num_rows)

    plt.figure(figsize = (10, 6))
    plt.bar(recent_rows['deposit date'], recent_rows['Net Pay'], color = 'blue')
    plt.xlabel('Deposit Date')
    plt.ylabel('Net Pay (Checking + Savings)')
    plt.title(f'Sum of Checking and Savings for the Last {num_rows} Deposits')
    plt.xticks(rotation = 45)
    plt.tight_layout()
    plt.show()


def total_saved(dataframe): 
    """
    Calculate the total amount saved based on the cumulative savings allocation column in the DataFrame.

    Args:
        dataframe (pd.DataFrame): DataFrame containing paystub data.

    Returns:
        float: Total amount saved.


    By Christian Bechmann - Pandas operations (filtering)
    """
    dataframe['Cumulative Savings'] = dataframe['savings'].cumsum()
    total_amount_saved = dataframe['Cumulative Savings'].iloc[-1]
    return total_amount_saved

if __name__ == "__main__":
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
    
    extractor = PayStubExtraction('','','','','')
    extracted_info = extractor.extract_from_file(filepath)
         
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
    
    file_path = 'bank.csv'
    df = pd.read_csv(file_path)
    total_amount_saved = total_saved(df)
    
    print(f'Total Amount Saved (Savings Account): ${total_amount_saved:.2f}')
    
    try:
        recent_income()
    except Exception as e:
        print(f"Error {e}")

