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
        
        self.bank_accounts = {}
        self.total_income = total_income
        
        if 0 <= checking_percent <= 1 and 0 <= savings_percent <= 1:
            self.checking_percent = checking_percent
            self.savings_percent = savings_percent
            
        else:
            raise ValueError("Percentage has to be within 0.0 to 1.0 and percentage needs to be a float")
        
        if checking_percent + savings_percent == 1:
            self.checking_percent = checking_percent
            self.savings_percent = savings_percent
            
        else:
            raise ValueError("Checking percent and savings percent must equal to 1") # Check this for correction
        

    def calculator(self):
        """Calculate and allocate income to checking and savings accounts.
        
        Returns:
            dict: the deposit amount to checking and savings account.
        """
        
        money_to_checking = self.total_income * self.checking_percent
        money_to_savings = self.total_income * self.savings_percent
        
        money_dict = {'checking': money_to_checking, 'savings': money_to_savings}

        self.bank_accounts = money_dict
        return self.bank_accounts
    
    
p = IncomeAllocator(5000, 0.2, 0.8)
p2 = IncomeAllocator(8000, 0.5, 0.5)
