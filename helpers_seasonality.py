from twelvedata import TDClient
import pandas as pd
from datetime import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()

def download_td_test(start_date = "2020-01-01", end_date = "24-05-10"):
    # Initialize client
    API_KEY = os.getenv("TD_API_KEY")
    td = TDClient(apikey = API_KEY)

    # Construct the necessary time series
    ts = td.time_series(
        symbol="AAPL",
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




