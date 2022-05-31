import yfinance as yf
import pandas as pd
#used to find which of two values are smaller  
print('*******'+__name__ + ' is called ********') #print when ever this file is called

def spot_lesser_val(value1,value2):
    if value1<value2:
        final_val=value1
    if value2<value1:
        final_val=value2
    if value1==value2:
        final_val=value1
    return final_val  

#gets daily open,close,high,low and add new column for the symbol from yfinance
#I/P 'AAPL,MSFT,AMD'
#I/P “1d”, “5d”, “1mo”, “3mo”, “6mo”, “1y”, “2y”, “5y”, “10y”, “ytd”, “max”
def Get_Daily_OCHL(tick_symbol,limit):
    sp500 = yf.Ticker(tick_symbol)         #get ticker name
    df_data = sp500.history(period=limit)  #get OCHL data
    df_data['Symbol']=tick_symbol              #add new column for ticker symbol 
    return df_data

#re-indexing-->remove whitespace-->replace space with underscore-->make capital letters
#I/P dataframe
def Clean_Dataframe_Columns(dataframe):
    if dataframe.index.name!=None:
        dataframe=dataframe.reset_index()        # re-indexing so date will become as a column
    dataframe.columns = dataframe.columns.str.strip() #remove whitespace
    dataframe.columns = dataframe.columns.str.replace(' ', '_') #replace space
    dataframe.columns = dataframe.columns.str.upper() #convert to upper case
    return dataframe

#pulls excel file from world bank URL and transpose the dataframe 
#I/P URL , column name for transposed data
def Get_WorldBank_Data_Via_Excel_URL(link,col_name):
    df_data = pd.read_excel(link)
    df_data = df_data.iloc[2:] #remove 1st 2 rows
    df_data.columns = list(df_data.iloc[0])[:4]+list(map(int, list(df_data.iloc[0])[4:])) # make row as column by converting years float to int
    df_data = df_data.iloc[1:]
    df_data=df_data.melt(id_vars=list(df_data.columns[:4]),var_name="Year", 
                           value_name=col_name) #transform coverting column to rows
    
    return df_data



