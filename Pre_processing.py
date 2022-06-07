# -*- coding: utf-8 -*-
"""
Created on Tue May 17 20:06:50 2022
@author: Shan
Purpose - clean and format the dataframe from different source
"""

import User_Defined_Fx as uf 
import pandas as pd
import numpy as np
##############################Pre Processing#######################################

#######################get country and index data##################################
indice_data=pd.read_csv('indice_country.csv',skipinitialspace = True)
#format the column
indice_data=uf.Clean_Dataframe_Columns(indice_data) #refer to user defined function
#fill/filter missing data
indice_data=indice_data[indice_data['COUNTRY'].notna()] #Remove NaN based on country column
indice_data['SHORT_NAME'] = indice_data['SHORT_NAME'].fillna(indice_data['NAME']) #fill short_name based on name column
#format the data
indice_data['INDICE_TYPE'] = indice_data['INDICE_TYPE'].str.title() #make first letter cap each words
indice_data['COUNTRY'] = indice_data['COUNTRY'].str.title() #make first letter cap in each words

#######################get Historical OCHL for each index#########################
#get daily Open,close,high,low data by using loop
All_OCHL_Data=pd.DataFrame()
for index, row in indice_data.iterrows():
    df_data=uf.Get_Daily_OCHL(row["TICKER_SYMBOL_YFINANCE"],'max') # get OCHL data
    All_OCHL_Data=All_OCHL_Data.append(df_data) #appending the dataframes
#format the column
All_OCHL_Data=uf.Clean_Dataframe_Columns(All_OCHL_Data) #refer to user defined function
#fill/filter missing data

#format the data
All_OCHL_Data['DATE']=All_OCHL_Data['DATE'].astype(str).str[:10] # triming time stamp from date

#######################get Historical GDP data for countries########################
WB_URL='https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=excel'
gdp_data=uf.Get_WorldBank_Data_Via_Excel_URL(WB_URL,'GDP_USD')
#format the column
gdp_data=uf.Clean_Dataframe_Columns(gdp_data) #refer to user defined function
gdp_data=gdp_data.dropna() # remove NaN values

##########################Get Inflation data for countries##########################
#world bank Excel URL - source - https://data.worldbank.org/indicator/FP.CPI.TOTL.ZG?locations=IN
WB_URL='https://api.worldbank.org/v2/en/indicator/FP.CPI.TOTL.ZG?downloadformat=excel'
infla_data=uf.Get_WorldBank_Data_Via_Excel_URL(WB_URL,'INFLATION_%')
#format the column
infla_data=uf.Clean_Dataframe_Columns(infla_data) #refer to user defined function
infla_data=infla_data.dropna() # remove NaN values

##########################Get countries code for Lookup Purpose#####################
country_code = pd.read_excel('https://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=excel')
country_code=country_code[country_code.columns[:2]].iloc[2:] #get 1st 2 column and remove 1st 2 rows
country_code.columns=country_code.iloc[0] #make first row as column
country_code=country_code.iloc[1:]#remove the first row

#################################End of Pre Processing##############################

df = All_OCHL_Data.groupby(['SYMBOL'])
# using agg() function on Date column
df2 = df.agg(MIN_DATE=('DATE', np.min))
#inner join
indice_data = pd.merge(indice_data, df2, left_on='TICKER_SYMBOL_YFINANCE', right_on='SYMBOL', how='inner')




