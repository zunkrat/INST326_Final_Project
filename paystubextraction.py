#Tulasi Venkat
import re

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

#Using PayStubExtraction to extract information from a paystub
file_path = "11_4_23_paystub.txt" 
with open(file_path, 'r') as file:
    text_content = file.read()

extracted_info = {key: re.search(pattern, text_content).group(1) for key, pattern in PayStubExtraction.patterns.items() if re.search(pattern, text_content)}
    
pay_stub_info = PayStubExtraction(
    direct_deposit_date = extracted_info.get('Direct Deposit Date', ''),
    employee_full_name = extracted_info.get('Employee Full Name', ''),
    current_earnings = extracted_info.get('Current Earnings', ''),
    current_taxes = extracted_info.get('Current Taxes', ''),
    net_pay = extracted_info.get('Net Pay', '')
    )
    
print(pay_stub_info.__dict__)
