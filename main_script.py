import Pre_processing 
#exec(open("./Pre_processing.py").read())
import pandas as pd
from numpy import array
##############################################################################

df_OCHL_data=Pre_processing.All_OCHL_Data
df_OCHL_data['NEW_HIGH_DIST']=''
# setting first value to start the loop
last_high,last_value,last_date=0.0 , df_OCHL_data['SYMBOL'][0] , df_OCHL_data['DATE'][0]
#creating new dataframe to store all new high days & start and end date of each new low levels
df_new_high = pd.DataFrame(columns=['DATE','SYMBOL','NEW_HIGH'])
df_fall_range = pd.DataFrame(columns=['SYMBOL','START_DATE','END_DATE','PERCENTAGE'])
#Array to find the position of CMP Current market price
a = array([10,15,20,25,30,35,40,50,60,70,80,90])
for index,row in df_OCHL_data.iterrows():
    if row.SYMBOL!=last_value:
        #update null end dates 
        df_fall_range.loc[(df_fall_range['SYMBOL'] == last_value)
              & (df_fall_range['END_DATE'] == "NULL")
              , 'END_DATE'] = last_date         
        #for new symbol reset value
        last_high,last_value=0.0 , row.SYMBOL
    if row.HIGH>=last_high:
        #touched new high
        #append the row df_new_high dataframe
        df_new_high.loc[len(df_new_high.index)] = [row.DATE, row.SYMBOL, row.HIGH] 
        df_OCHL_data.at[index,'NEW_HIGH_DIST']=0 #updating the row
        last_high=row.HIGH
    else:
        # not a new high
        df_OCHL_data.at[index,'NEW_HIGH_DIST']=(1-(row.CLOSE/last_high))*100 #updating the percentage
        #check if the low falls below 10%
        low_percent=(1-(row.LOW/last_high))*100 #caluculating the percentage
        current_per_list=list(a[a <= low_percent ]) #find position of current day %
        if len(current_per_list)>0:
            #check if any increase in the percentage, then update the end date
            df_fall_range.loc[(df_fall_range['SYMBOL'] == row.SYMBOL)
                              & (df_fall_range['END_DATE'] == "NULL")
                              & (df_fall_range['PERCENTAGE'] > current_per_list[-1])
                              , 'END_DATE'] = row.DATE   
            #get null valued data from the new df_fall_range dataframe
            list_symbol_row=df_fall_range[(df_fall_range.SYMBOL == row.SYMBOL) & (df_fall_range.END_DATE == "NULL")]
            get_per_column=list(list_symbol_row['PERCENTAGE'])
            #check if any new entry to be added in df_fall_range dataframe
            non_match = list(set(get_per_column)-set(current_per_list)) + list(set(current_per_list)-set(get_per_column))  
            non_match=list(sorted(set(non_match)))
            if len(non_match)>0:
                for i in non_match:
                    df_fall_range.loc[len(df_fall_range)] = [row.SYMBOL,row.DATE,'NULL',i]
        else:
            #updating all rows when recovered from 10% fall
            df_fall_range.loc[(df_fall_range['SYMBOL'] == row.SYMBOL)
                  & (df_fall_range['END_DATE'] == "NULL")
                  & (df_fall_range['PERCENTAGE'] > 10)
                  , 'END_DATE'] = row.DATE         
    last_value,last_date=row.SYMBOL,row.DATE
    #end of for loop

