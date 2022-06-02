
import pandas as pd

bank_df=pd.read_csv('Kar.csv',skipinitialspace = True)

#moving the duplicate records to different dataframe
error_duplicate=bank_df.loc[bank_df[['BankID','AccountID']].duplicated(), :]
#removing duplicate to retain unique combination
new_dff = bank_df.drop_duplicates(subset=['BankID','AccountID'])

#function to check business condition
def check_error(account_id):
    if len(account_id) < 7 or len(account_id) > 11:
        error_flag='Y'
        reason='Char length <7 or >11'
        print('first conditiin')
    elif account_id[1:].isnumeric() is False:
        error_flag='Y'
        reason='contains alphabets after first letter'
    elif account_id[0].upper() not in ['C','S','D']:
        error_flag='Y'
        reason="Dosnt have first char 'C','S','D'"
    else:
        error_flag='N'
        reason=account_id[0].upper()
    return [error_flag,reason]

   
#sample testing
#df_OCHL_data=pd.read_csv('All_OCHL_data.csv',skipinitialspace = True)

import seaborn as sns
tips=sns.load_dataset("tips")