import pandas as pd


bank_accounts = {
    
    'checking': 500.00,
    'savings': 400.00
}


def dic_csv(dict = None):
    
    """
    Transforms the dictionary of the bank accounts into a csv file for filtering
    
    Args:
    
    dict (dictionary):
        A dictionary to turn into a csv file
        
    """
    
    df = pd.DataFrame([dict])
    df.to_csv('bank.csv', index = False)
    
    return df

p = dic_csv(bank_accounts)
