import baostock as bs
import pandas as pd
from googletrans import Translator
#### login system####
lg = bs.login()
translator = Translator()
# Display login return information
print('login respond error_code:'+lg.error_code)
print('login respond error_msg:'+lg.error_msg)

# Get CSI 500 constituent stocks
rs = bs.query_zz500_stocks("2021-01-01")
print('query_zz500 error_code:'+rs.error_code)
print('query_zz500 error_msg:'+rs.error_msg)
#Print the result set
zz500_stocks = []
while (rs.error_code == '0') & rs.next():
    # Get a record and merge the records together
    zz500_stocks.append(rs.get_row_data())
result = pd.DataFrame(zz500_stocks, columns=rs.fields)

#apply translator to column code_name
result['english_code'] = result['code_name'].apply(lambda x: translator.translate(x, src='auto', dest='en').text )
print(result)
#### Output the result set to a csv file
result.to_csv("csi500.csv", index=False)
# Log out of the system
bs.logout()