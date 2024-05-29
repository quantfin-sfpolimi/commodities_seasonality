# Libraries used
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from twelvedata import TDClient 
from dotenv import load_dotenv 
import os

#TODO: added docstrings + error handling + fixed some spaghetti code + generalized a function
class Asset:
    """
    Represents an asset, such as an ETF (Exchange-Traded Fund), with associated data and functionality.

    Attributes:
    - type (str): The type of the asset (e.g., 'ETF', 'Stock', 'Bond').
    - ticker (str): The ticker symbol or identifier of the asset.
    - full_name (str): The full name or description of the asset.
    - df (pandas.DataFrame): The DataFrame containing historical data of the asset.
    - index_name (str): The name of the index that the asset tracks (if applicable).
    - ter (float): The Total Expense Ratio (TER) of the asset.

    Methods:
    - apply_ter(ter): Apply a specified TER to adjust the asset's historical data.
    - update_from_html(extraction_type): Update asset attributes (e.g., ISIN, TER) by extracting
      information from HTML data based on the specified extraction type ('isin' or 'ter').
    - update_index_name(): Update the index name of the asset by extracting information from a webpage
      based on its ISIN (International Securities Identification Number).
    """
    
    def __init__(self, type, ticker, full_name):
        self.type = type
        self.ticker = ticker
        self.df = None
        self.full_name = full_name
        self.index_name = None
        self.ter = None
        self.isin = None

    def _extract_value_from_html(self, data, start_pattern, end_pattern):
        """
        Extracts a value from HTML data based on start and end patterns.

        Parameters:
        - data (str): HTML data to search within.
        - start_pattern (str): Pattern indicating the start of the value.
        - end_pattern (str): Pattern indicating the end of the value.

        Returns:
        - str: Extracted value between start and end patterns, or None if not found.
        """
        with open('./very_long_html.txt', 'r') as file:
            data = file.read()
        start_index = data.upper().find(self.full_name.upper(), 0)
        if start_index == -1:
            return None

        value = ""
        index = start_index + len(start_pattern)
        while index < len(data):
            if data[index] == end_pattern:
                break
            value += data[index]
            index += 1

        return value
    
    def apply_ter(self, ter):
        """
        Applies a specified Total Expense Ratio (TER) adjustment to the historical data of the asset.

        Parameters:
        - ter (float): The Total Expense Ratio (TER) to apply.
        
        """
        if self.ticker not in self.df.columns:
            raise ValueError(f"Ticker '{self.ticker}' not found in DataFrame columns.")

        monthly_ter_pct = (ter / 12) / 100
        columns = self.df[self.ticker]
        new_df = columns.apply(lambda x: x - monthly_ter_pct)
        self.df[self.ticker] = new_df

    def update_from_html(self, extraction_type):
        """
        Updates ETF attributes (e.g., ISIN, TER) by extracting information from HTML data.

        Parameters:
        - extraction_type (str): Type of extraction ('isin' or 'ter').

        Returns:
        - str: Extracted value, or None if extraction is unsuccessful.
        """
        if extraction_type not in ['isin', 'ter']:
            raise ValueError("extraction_type must be either 'isin' or 'ter'.")

        with open('./very_long_html.txt', 'r') as file:
            data = file.read().replace('\n', '')

        if extraction_type == 'isin':
            value = self._extract_value_from_html(data, self.full_name, '"')
            self.isin = value
        elif extraction_type == 'ter':
            if self.isin is None:
                raise ValueError("ISIN is required to extract TER.")
            value = self._extract_value_from_html(data, self.isin, '"%')
            self.ter = value


    def update_index_name(self):
        if self.isin is None:
            raise ValueError("ISIN is required to update index name.")

        url = f"https://www.justetf.com/it/etf-profile.html?isin={self.isin}"
        options = Options()
        options.add_argument("--headless")
        browser = webdriver.Chrome(options=options)
        browser.get(url)

        html = browser.page_source
        self.index_name = self._extract_value_from_html(html, "replica l'indice", '.')

        browser.quit()
        
    def load_df(self):
        load_dotenv()
        API_KEY = os.getenv('API_KEY')
        td = TDClient(apikey=API_KEY)
        # twelve data tickers don't include the name of the exchange (eg: VUAA.MI would simply be VUAA)
        if "." in self.ticker:
            ticker = self.ticker[0:self.ticker.rfind(".")]
        else:
            ticker = self.ticker

        df = td.time_series(
            symbol=ticker,
            interval="1month",
            #start_date="2019-01-01",
            #end_date="2020-02-02",
            timezone="America/New_York"
        )

        # Returns pandas.DataFrame
        self.df = df.as_pandas()

    def load(self):
        if self.type == 'ETF':
            self.update_from_html('isin')
            self.update_from_html('ter')
            self.update_index_name()
        self.load_df()
    
    def info(self):
        print("Full name: ", self.full_name)
        print("Ticker: ", self.ticker)
        print("Type: ", self.type)
        print("Ter: ", self.ter, "%")
        print("Index name: ", self.index_name)
        print("Isin: ", self.isin)
        print("Dataframe: \n", self.df)

    