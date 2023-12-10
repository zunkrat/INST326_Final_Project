
# These functions run under the assumption that we have a CSV file with date rows and columns with the below names
# net pay, taxes, checking allocation, savings allocation, entertainment allocation,
# groceries allocation, travel allocation, transportation allocation, recreation allocation, 
# housing allocation, and other allocation
import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
import matplotlib.pyplot as plt

def recent_income(csv_file, num_rows=10):
    """
    Plot the net pay for the specified number of most recent paystubs from a CSV file.

    Args:
        csv_file (str): Path to the CSV file containing paystub data.
        num_rows (int): Number of most recent paystubs to include in the plot.

    Returns:
        None
    """
    df = pd.read_csv(csv_file)
    selected_columns = ['Date', 'Net Pay']
    df = df[selected_columns]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date', ascending=False)
    recent_rows = df.head(num_rows)

    plt.figure(figsize=(10, 6))
    plt.bar(recent_rows['Date'], recent_rows['Net Pay'], color='blue')
    plt.xlabel('Date')
    plt.ylabel('Net Pay')
    plt.title(f'Net Pay for the Last {num_rows} Paystubs')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Example usage
recent_income('file.csv')

def total_saved(dataframe): 
    """
    Calculate the total amount saved based on the cumulative savings allocation column in the DataFrame.

    Args:
        dataframe (pd.DataFrame): DataFrame containing paystub data.

    Returns:
        float: Total amount saved.
    """
    dataframe['Cumulative Savings'] = dataframe['Savings Allocation'].cumsum()
    total_amount_saved = dataframe['Cumulative Savings'].iloc[-1]
    return total_amount_saved

total_amount_saved = total_saved(df)
print(f'Total Amount Saved: ${total_amount_saved:.2f}')

def compare_category_allocations(dataframe, categories):
    """
    Compare the percentage allocations for specified categories over time.

    Args:
        dataframe (pd.DataFrame): DataFrame containing paystub data.
        categories (list): List of category names to compare.

    Returns:
        None
    """
    relevant_columns = ['Date', 'Net Pay', 'Taxes', 'Checking Allocation', 'Savings Allocation'] + categories
    filtered_df = dataframe[relevant_columns]

    for category in categories:
        filtered_df[category] = pd.to_numeric(filtered_df[category].str.rstrip('%'), errors='coerce')

    grouped_df = filtered_df.groupby('Date')[categories].mean()

    plt.figure(figsize=(12, 6))
    for category in categories:
        plt.plot(grouped_df.index, grouped_df[category], label=category)

    plt.title('Comparison of Category Allocations Over Time')
    plt.xlabel('Date')
    plt.ylabel('Percentage Allocation')
    plt.legend()
    plt.show()

# Example usage
compare_category_allocations(df, categories=['Entertainment', 'Groceries', 'Travel', 'Housing', 'Other'])