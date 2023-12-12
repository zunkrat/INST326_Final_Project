# INST326_Final_Project

    Explanation of the purpose of each file in the repository:
       
        [10_21_23_paystub.txt, 10_7_23_paystub.txt, 11_4_23_paystub.txt,
        8_26_23_paystub.txt, 9_23_23_paystub.txt]: 
        These are text files of Christian's paystubs from the corresponding dates in the format that was used to         create the regular expressions, so extraction from other paystubs with a different format           
        might not be accurate.

        bank.csv: The "bank.csv" is the CSV file that the program creates and writes paystub extraction information with the inputted allocations to. This file has three columns with
        one row per paystub entry with savings, checking, and date. 
        
        final_project.py: This file contains our final project script in its entirety. This script takes a paystub in text format and reads the information in it using regular 
        expressions. 
        Additionally, this script allows the user to input the percentage of income in a paystub they wish to allocate to their checking and savings. 
        The calculations of these percentages are stored in a dictionary and written in a CSV file. The CSV file is then used to create visualizations and utilize a filtering function 
        to calculate the total the user has saved. 
    
    How to run the program from the command line:
    
    
    How to use the program and/or interpret the output of the program: 
    
    

    | Method/Function          | Primary Author | Techniques Demonstrated                                 |
    |--------------------------|----------------|---------------------------------------------------------|
    | func extract_paystub_info| Tulasi         | regular expressions                                     |
    | func extract_from_file   | Tulasi         | 'with' statemets                                        |
    | func calculator          | Gwon           | conditional expressions                                 |
    | func user_allocation     | Ojie           | Set operations on sets or frozensets                    |
    | func get_percentage_input| Ojie           | Optional parameters and/or keyword arguments            |
    | func main                |                |                                                         |
    | func parse_args          | Gwon           | the ArgumentParser class from the argparse module       |
    | func dic_csv             |                |                                                         |
    | func recent_income       | Christian      | visualizing data with pyplot or seaborn                 |
    | func total_saved         | Christian      | filtering operations using Pandas                       |

