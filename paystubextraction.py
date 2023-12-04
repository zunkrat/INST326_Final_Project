import re

class PayStubExtraction:
    def __init__(self, direct_deposit_date, employee_full_name, current_earnings, current_taxes, net_pay):
        self.direct_deposit_date = direct_deposit_date
        self.employee_full_name = employee_full_name
        self.current_earnings = current_earnings
        self.current_taxes = current_taxes
        self.net_pay = net_pay
        
    patterns = {
        'Direct Deposit Date': r'Paid by DIRECT DEPOSIT on (\d{2}-\d{2}-\d{4})',
        'Employee Full Name': r'(\w+ \w+ \w+)  \n',
        'Current Earnings': r'Earnings\n-\nTaxes\n-\nDeductions\n=\nNet Pay\nCurrent\n\s+(\d+\.\d{2})',
        'Current Taxes': r'Earnings\n-\nTaxes\n-\nDeductions\n=\nNet Pay\nCurrent\n\s+\d+\.\d{2}\n\s+(\d+\.\d{2})',
        'Net Pay': r'Net Pay\nCurrent\n\s+\d+\.\d{2}\n\s+\d+\.\d{2}\n.+\n\s+(\d+\.\d{2})'
    }

file_path = "converted_pay_stub.txt" 
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