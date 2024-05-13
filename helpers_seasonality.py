from twelvedata import TDClient
import pandas as pd
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv

load_dotenv()

def concat_data(td, end_date, output_size, ticker, interval):

    data_to_load_tmp = output_size
    tmp_data = end_date
    parts = []
    concat = 0
    flag = 0

    for i in range(0, (output_size // 5000)+1):

        # activate only if output_size is grater than 5000
        if (data_to_load_tmp >= 5000):
            print('downloading with concatenation')
            ts = td.time_series(
                symbol=ticker,
                interval=interval,
                outputsize=5000,
                end_date = tmp_data,
                timezone="America/New_York",
            ).as_pandas()
            data_to_load_tmp -= 5000
            parts.append(ts)
            tmp_data = parts[i-1].index.tolist()[-1] - timedelta(days=1)
            concat = 1

        # activate when output_size is smaller than 5000 or to download the last part of the concatenated df
        if (data_to_load_tmp < 5000 and flag == 0):
            print('downloading without concatenation')
            ts = td.time_series(
                symbol=ticker,
                interval=interval,
                outputsize=data_to_load_tmp,
                end_date = tmp_data,
                timezone="America/New_York",
            ).as_pandas()
            parts.append(ts)
            flag = 1
    
    # if the df has multiple parts it returns it else it returns only the simple df
    if(concat == 1):
        print(concat)
        print(parts)
        return pd.concat(parts)
    else:
        return parts[0]
    

def download_td(start_date, end_date, ticker):
    # Initialize client
    API_KEY = os.getenv("TD_API_KEY")
    td = TDClient(apikey = API_KEY)

    #time format for strptime function
    date_format = "%Y-%m-%d"

    #outputsize, timedelta between end_date and start_date
    output_size = (parser.parse(end_date) - parser.parse(start_date)).days
    print(output_size)

    # Construct the necessary time series and Returns pandas.DataFrame
    data = concat_data(td, start_date, end_date, output_size, ticker, '1day')
    
    tmp = datetime.strptime(start_date, date_format)

    #slicing dataframe> if the final is an holiday day, it add a day until it find it as a tarding day
    while True:
        try:
            return data.iloc[:data.index.get_loc(tmp)]
        except:
            tmp = tmp + timedelta(days=1)

def manage_seasonality(input_dataframe, excluded_years = []):
    min_years_local = 1


    stock_dataframe = input_dataframe.copy()

    years_array = pd.to_datetime(stock_dataframe.index).year.unique()
    days_array = [*range(1, 365, 1)]

    stock_dataframe["year"] = pd.to_datetime(stock_dataframe.index).year
    #stock_dataframe["day"] = 0

    #check if enough years:
    if (len(years_array) - len(excluded_years)) < min_years_local:
        print("Error, insert more years")
        return False

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

      epoch = time.mktime(new_date.timetuple())
      dataframe.at[row,"epoch"] = epoch

    dataframe = dataframe.iloc[:, ::-1]
    print(dataframe)
    return dataframe.values.tolist()