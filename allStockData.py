import baostock as bs
import pandas as pd

#### login system####
lg = bs.login()
# Display login return information
print('login respond error_code:'+lg.error_code)
print('login respond error_msg:'+lg.error_msg)

#### Obtain historical K-line data of all the codes present in csi500.csv####
# Read the stock code in the csi500.csv file
stock_code = pd.read_csv("csi500.csv")
# Convert the stock code to a list
stock_code_list = stock_code["code"].tolist()
# Define a list to store the data of each stock
stock_data_list = []
# Loop through each stock code to get the historical K-line data
for code in stock_code_list:
    # Get the historical K-line data of the stock
    rs = bs.query_history_k_data_plus(code,
        "date,time,code,open,high,low,close,volume,amount,adjustflag",
        start_date='2022-04-01', end_date='2022-07-31',
        frequency="30", adjustflag="3")
    print('query_history_k_data_plus respond error_code:'+rs.error_code)
    print('query_history_k_data_plus respond error_msg:'+rs.error_msg)
    # Store the data of each stock in the list
    while (rs.error_code == '0') & rs.next():
        stock_data_list.append(rs.get_row_data())
# Define the column name of the data frame
stock_columns = ["date","time","code","open","high","low","close","volume","amount","adjustflag"]
# Convert the list to a data frame
stock_data = pd.DataFrame(stock_data_list, columns=stock_columns)
print(stock_data)
# Output the data frame to a csv file
stock_data.to_csv("all_stock_data.csv", index=False)

#### Log out of the system####
bs.logout()