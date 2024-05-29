# Libraries used
#FIXME: are all of these used? if not, **delete them**
import datetime as dt
import numpy as np
import os
import pandas as pd
import pickle
import yfinance as yf #FIXME: why is yfinance being used? 
from matplotlib import pyplot as plt
import matplotlib.colors
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.request import urlopen
from datetime import datetime
import math

def createURL(url, name):
    ''' 
    Given a url and name of an index it creates the correspondant url
    Parameters: url, name (Strings)
    Returns: url (String)
    '''

    for word in name.split():
        if '®' in word:
            word=word[0:-1]

        # & letter cannot be part of a link, %26 to substitute
        if word == "S&P":
            word = "S%26P"

        url += word + "%20"
    return url[:-3] + ".csv"

# port
def get_index_prices(name, ticker):
    '''
    Given an index name and the ticker of an ETF that tracks it, the function
    looks for the index data and returns it in a Dataframe format
    Parameters:
    - name: String
    - ticker: String
    Returns:
    - return_data: pandas Dataframe
    '''

    url_list = ["countries/", "curvo/", "countries_small_cap/", "indexes_gross/", "regions_small_cap/"]
    url_base = "https://raw.githubusercontent.com/NandayDev/MSCI-Historical-Data/main/"

    # trying different paths to the find index data
    response = None
    for url_end in url_list:
        url = createURL(url_base + url_end, name)
        try:
            response = urlopen(url)
        except:
            continue
        break

    # if no index found return None
    if response == None:
        return None

    # converting the response data to a pandas Dataframe
    return_data = pd.read_csv(response, sep=",", names=["Date", ticker], skiprows=1)
    #FIXME: why yfinance ;-; 
    # yahoo finance date format is "2024-04-01", whereas the index data we have has a "2024-04" format
    return_data["Date"] += "-01"

    return return_data

def get_first_date_year(all_dates):
    ''' #FIXME: change docstring
    This function, named get_first_date_year, takes as input a list of 
    dates called all_date. The function returns a list of strings 
    representing the first dates of each year present in the all_date list.
    
    Parameters:
        - all_dates: Time_stamp array
            List of dates
    '''
    current_year = int(str(all_dates[0])[:4])
    date=[]
    for i in range(0, len(all_dates)):
        if current_year == int(str(all_dates[i])[:4]):
            date.append(str(all_dates[i])[:10])
            current_year+=1
    return date


class Portfolio:
    def __init__(self, assets, weights, df, tickers):
        self.assets = assets
        self.weights = weights
        self.df = df
        self.tickers = tickers

    
    def update_tickers(self):
        ###
        return 
    
    def update_index_names(self):
        ###
        return
    
    def create_df(self):
        '''
        Given the portfolio_tickers and index_names lists the function gets the correspondant index name of each ETF.
        Then, it joins the older index data to the newer ETF data month by month (in % change), so that we have more historical data
        for ETFs. It returns the portfolio_prices dataframe with the older index data added to it.

        Parameters:
        - portfolio_tickers [List of Strings]
        - index_names [List of Strings]

        Returns:
        - portfolio_prices [Dataframe]
        '''
        portfolio_tickers = self.update_tickers()
        index_names = self.update_index_names()

        portfolio_tickers.append("IBM") #FIXME: ?
        portfolio_prices = yf.download(portfolio_tickers, interval='1mo')['Open'] #FIXME: yfinance 
        portfolio_prices = portfolio_prices.pct_change() #FIXME: does this work?

        for i in (i for i in range(0,len(index_names)-1) if index_names[i] != ""): #FIXME: for i in i in i >> for i in range(len(index_names) - 1):
            ticker = portfolio_tickers[i]
            return_data = get_index_prices(index_names[i], ticker)
            return_data[ticker] = return_data[ticker].pct_change()

            for i in range(0,len(return_data)):
                return_data.loc[i,"Date"] = datetime.strptime(return_data.loc[i,"Date"], '%Y-%m-%d')

            return_data.set_index("Date", inplace = True)
            portfolio_prices[ticker].fillna(return_data[ticker], inplace = True) #FIXME: why fillna
        
        portfolio_prices.drop("IBM", axis=1, inplace = True)
        portfolio_prices.dropna(axis = 0, how = 'all', inplace = True)

        self.df = portfolio_prices
    
    def annual_portfolio_return(self):
        '''
        The function annual_portfolio_return calculates the annual return of 
        a portfolio based on the provided stock symbols and their respective 
        weights. It utilizes historical stock price data downloaded from Yahoo Finance, 
        computes the annual percentage returns for each stock in the portfolio, 
        and then calculates the weighted average portfolio return for each year.
        
        Parameters:
            - portfolio_prices: pandas.DataFrame
                It's a dataframe that contains the opening prices of stocks, 
                with tickers as columns and dates as rows.
            - portfolio_tickers: string array
                Array containing the tickers of all assets in the portfolio.
            - portfolio_weight: float array
                Array containing the weights of the various stocks.
        Returns:
            - pandas.DataFrame
                DataFrame containing the annual returns (%) of the portfolio with 
                the year as the index and the returns as the only column.
        '''


        
        all_dates=(list(self.df.index))
        date = get_first_date_year(all_dates)
        
        portfolio_year = pd.DataFrame(columns=self.tickers)
        for i in range(0, len(date)):
            portfolio_year.loc[date[i]]=self.df.loc[date[i]]
        
        stocks_yield = portfolio_year.pct_change().dropna(how='any')
        year_yield=pd.DataFrame(columns=['Yield'])

        for i in range(len(stocks_yield.index)):
            mean_yield=0
            for j in range(len(self.tickers)):
                mean_yield+=stocks_yield.iloc[i][self.tickers[j]]*self.weights[j]
            year_yield.loc[str(date[i])[:4]]=mean_yield*100

        return year_yield
    
    def monthly_portfolio_return(self):
        '''
        This function outputs a dataframe containing the monthly portfolio return of a list of assets. 
        Parameters:
            - portfolio_prices [Dataframe], containing the monthly(!) value of all assets
            - portfolio_tickers [list of Strings]
            - portfolio_weight [list of floats]
        Returns:
            - month_yield [Dataframe]
        '''

        date=list(self.df.index)
        stocks_yield = self.df.pct_change().dropna(how='any') 
        month_yield=pd.DataFrame(columns=['Yield'])

        for i in range(len(stocks_yield.index)):
            mean_yield=0
            for j in range(len(self.tickers)):
                mean_yield+=stocks_yield.iloc[i][self.tickers[j]]*self.weights[j]
            month_yield.loc[str(date[i])[:7]]=mean_yield*100
        return month_yield

    def portfolio_return_pac(self, starting_capital, amount, fee, fee_in_percentage):
        '''
        The portfolio_return_pac function outputs a Dataframe with the monthly value of a portfolio built using a PAC (Piano di Accumulo di Capitale) strategy.
        The user can input a starting_capital (initial amount of money in the portfolio), the amount of money that he/she invests each month and a broker's fee.
        If the fee is a fixed amount for each new contribution the percentage parameter should be set as False. If the fee is based on a percentage of the
        contribution the percentage parameter should be set as True.
        Parameters:
            - portfolio_prices [Dataframe], containing the monthly(!) value of all assets
            - portfolio_tickers [list of Strings]
            - portfolio_weight [list of floats]
            - starting_capital [int]
            - amount [int]
            - fee [int]
            - percentage [boolean]
        Returns:
            - capital_df [Dataframe]
        '''
        
        # set variables up
        month_yield = self.monthly_portfolio_return()
        capital = starting_capital
        capital_df = pd.DataFrame(columns=['Capital'])
        date=list(month_yield.index)

        for i in range(len(date)):
            # for each month, add the amount variable to the capital and subtract the fee 
            if fee_in_percentage:
                capital += amount - amount*fee/100
            else:
                capital += amount - fee

            # update the capital variable according to the portfolio performance that month
            capital += month_yield["Yield"].iloc[i]*capital/100

            # then, update the capital_df dataframe by filling the corresponding month with the new capital value
            capital_df.loc[str(date[i])[:7]] = capital

        return capital_df 


    def graph_plot(self):
        '''
            This function, named graph_plot, generates a representative 
            graph of the portfolio values based on the dates provided 
            in the portfolio_prices dictionary.
            
            Parameter:
                - portfolio_prices : Dictionary
                    A dictionary containing the portfolio value with corresponding dates as indices.
        '''

        all_dates=list(self.df.keys())
        date=get_first_date_year(all_dates)
        date.append(str(all_dates[len(all_dates)-1])[:10])

        plt.style.use("ggplot")
        plt.plot(list(self.df.keys()), list(self.df.values()))
        plt.xticks(date,  rotation=45)
        plt.show()

    def MDD(self):
        '''
            This function, named MDD (Maximum Drawdown), calculates the maximum 
            drawdown of a portfolio based on the portfolio prices provided as input.
            
            Parameters:
                - portfolio_prices: Dictionary
                    A dictionary containing the portfolio value with corresponding dates as indices.
            
            Return:
                - float
                    Maximum Drawdown (%)
        '''
        value=list(self.df.values())
        return ((max(value)-min(value))/max(value))*100
        