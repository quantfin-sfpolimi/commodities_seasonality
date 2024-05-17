from twelvedata import TDClient
import pandas as pd
from datetime import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()

def download_td_test(start_date, end_date, ticker):
    # Initialize client
    API_KEY = os.getenv("TD_API_KEY")
    td = TDClient(apikey = API_KEY)

    # Construct the necessary time series
    ts = td.time_series(
        symbol=ticker,
        interval="1day",
        outputsize=2000,
        timezone="America/New_York",
        start_date = start_date,
        end_date = end_date
    )

    # Returns pandas.DataFrame
    data = ts.as_pandas()
    return data

def manage_seasonality(input_dataframe, excluded_years = []):
    
    stock_dataframe = input_dataframe.copy()

    years_array = pd.to_datetime(stock_dataframe.index).year.unique()
    days_array = [*range(1, 365, 1)]

    stock_dataframe["year"] = pd.to_datetime(stock_dataframe.index).year
    #stock_dataframe["day"] = 0

    for row, index in stock_dataframe.iterrows():
        #calculate day of the year of each date
        day = pd.to_datetime(row).timetuple().tm_yday
        stock_dataframe.at[row, "day"] = int(day)


    stock_dataframe["date"] = stock_dataframe.index
    stock_dataframe.set_index("day", inplace = True)
    stock_dataframe["close"] = stock_dataframe["close"].rolling(5).mean()


    returns_dataframe = pd.DataFrame(columns=years_array, index = days_array)

    for year in years_array:
      if year not in excluded_years:
            returns_dataframe[year] = (stock_dataframe.loc[stock_dataframe["year"] == year, "close"] - stock_dataframe.loc[stock_dataframe["year"] == year, "close"].iloc[-1]) / stock_dataframe.loc[stock_dataframe["year"] == year, "close"].iloc[-1]

    returns_dataframe.drop(excluded_years, axis = 1, inplace=True)
    returns_dataframe.bfill(inplace=True)

    return returns_dataframe

def calculate_seasonality(input_dataframe, excluded_years=[]):


  seasonal_dataframe = input_dataframe.copy()
  seasonal_dataframe.drop(excluded_years, axis = 1, inplace = True)


  return seasonal_dataframe.mean(axis = 1).to_frame()

def return_json_format(input_dataframe):
    """Given a price time dataframe with n dates, return json object with a [n x 2] array, containing for each
    date an array with timestamp and price.
    This is the suitable format to stockcharts with HighCharts

    Args:
        price_timeserie_dataframe (pandas dataframe): pandas dataframe with price of asset class on given dates
    Returns:
        Json object with array with timestamp format dates and price.
    """

    dataframe = input_dataframe.copy()
    

    for row, index in dataframe.iterrows():
        new_date = datetime.strptime("2024"+"-"+str(row), "%Y-%j")#.strftime("%m-%d-%Y")
        #print(new_date)
        
        epoch = int(time.mktime(new_date.timetuple()) * 1000)
        dataframe.at[row,"epoch"] = epoch

    dataframe = dataframe.iloc[:, ::-1]

    dataframe_list = dataframe.values.tolist()

    return dataframe_list

def check_years(startend):
    string = str(startend)

    start = int(string[:4])
    end = int(string[4:])
    
    if (end-start) < 4:
        return False
    
    return True
    
def plot_seasonality(startend, ticker):
    
    
    string = str(startend)
    start = string[:4]
    end = string[4:]
    
    
    start_date = start + "-01-01"
    end_date = end + "-01-01"
    
    df1 = download_td_test(start_date, end_date, ticker)
    df2 = calculate_seasonality(manage_seasonality(df1))
    
    final_json = return_json_format(df2)
    
    return final_json
    
def plot_single_year(startend,ticker):
    string = str(startend)

    start = int(string[:4])
    end = int(string[4:])
    
    single_year_data = {}
    

    for i in range(start,end-1):
        single_startend =  int(str(i)+str(i+1))
        
        single_year_data[i] = plot_seasonality(single_startend, ticker)
    
    return single_year_data

def stdev_seasonality(input_dataframe):
    
    dataframe = input_dataframe.copy()
    
    for row, index in dataframe.iterrows():
        #calculate day of the year of each date
        day = pd.to_datetime(row).timetuple().tm_yday
        dataframe.at[row, "day"] = int(day)
    
    months_serie = pd.Series(pd.date_range("2024-01-01", periods=12, freq="m"))
    stdev_seasonality_dataframe = pd.DataFrame(index=months_serie)
    stdev_seasonality_dataframe["STDEV"] = 0
    
    
    
    for row, index in stdev_seasonality_dataframe.iterrows():
        #calculate day of the year of each date
        day = pd.to_datetime(row).timetuple().tm_yday
        stdev_seasonality_dataframe.at[row, "day"] = int(day)
    

    stdev_seasonality_dataframe.set_index(stdev_seasonality_dataframe["day"], inplace=True)
    
    for x in stdev_seasonality_dataframe["day"]:
        temp = dataframe["close"].loc[dataframe["day"] == x]
        print(temp)
        stdev_current = temp.std()
        stdev_seasonality_dataframe.at[x, "STDEV"] = stdev_current
    
    print(stdev_seasonality_dataframe)

df1_test = download_td_test("2020-01-01", "2024-01-01", "AAPL")
d2_test = (manage_seasonality(df1_test))



def monthly_calculations(dataframe):
    dataframe = dataframe["close"]
    
    months_serie = pd.Series(pd.date_range("2024-01-01", periods=12, freq="m"))
    monthly_df = pd.DataFrame(index=months_serie)
    monthly_df["stdev"] = 0.0
    monthly_df["mean"] = 0.0
    
    monthly_dataframe = pd.DataFrame()
    
    monthly_dataframe["price"] = dataframe.resample('M', label = "right").last()
    monthly_dataframe["variation"] = monthly_dataframe.pct_change()
    
    for x in range(1,12):
        temp = monthly_dataframe.loc[monthly_dataframe.index.month == x]
        
        monthly_df.loc[monthly_df.index.month == x, "mean"] = temp["variation"].mean()
        monthly_df.loc[monthly_df.index.month == x, "stdev"] = temp["variation"].std()
        
        

    return monthly_df    
    
    
    
    
monthly_test = (monthly_calculations(df1_test))
def convert_high_chart_list(input_dataframe):


    dataframe = input_dataframe.copy()
    dataframe["epoch"] = 0.0
    dataframe_list = []
    for row, index in dataframe.iterrows():
    
        
        epoch = int(time.mktime(row.timetuple()) * 1000)
        dataframe.at[row,"epoch"] = epoch

    print(dataframe)
    dataframe = dataframe.iloc[:, ::-1]
    #print(dataframe.columns)
    for column in dataframe.columns:
        if column != "epoch":
            temp = dataframe.loc[:, ["epoch",column]]
            print(temp.values.tolist())
        
            dataframe_list.append(temp.values.tolist())
        


    return dataframe_list

