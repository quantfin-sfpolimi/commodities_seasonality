from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Optional
import json

from helpers_seasonality import *

app = FastAPI()

def change_ticker(ticker):
    commodities = ['XAU', 'XG', 'XBR', 'XPT']
    
    if ticker in commodities:
        return ticker + "/USD"
    else:
        return ticker

@app.get('/')
async def hello_world():
    return {"Msg": "Hello World!"}

""""
@app.get('/get-seasonality/{ticker}/{startend}')
async def get_seasonality(startend: int, ticker: str):

    string = str(startend)

    start = string[:4]
    end = string[4:]

    ticker = change_ticker(ticker)
    
    start_date = start + '-01-01'
    end_date = end + '-01-01'

    df = download_td_test(start_date = start, end_date = end, ticker = ticker)
    df1 = manage_seasonality(df)
    df2 = calculate_seasonality(df1)
    finale = return_json_format(df2)


    return finale


@app.get('/get-seasonality/{ticker}/{startend}/history')
async def get_seasonality(startend: int, ticker: str):
    ticker = change_ticker(ticker)
        
    df = plot_single_year(startend=startend, ticker=ticker)
    return df

@app.get('/get-seasonality/{ticker}/{startend}/monthly')
async def get_monthly_returns(startend: int, ticker: str):
    data = monthly_returns(startend = startend, ticker = ticker)
    return data


@app.get('/get-seasonality/{ticker}/{startend}/stdev')
async def get_monthly_returns(startend: int, ticker: str):
    data = monthly_stdev(startend = startend, ticker = ticker)
    return data
"""




default_start = 2000
default_end = 2022


def change_ticker(ticker):
    commodities = ['XAU', 'XG', 'XBR', 'XPT']
    
    if ticker in commodities:
        return ticker + "/USD"
    else:
        return ticker



@app.get('/get-seasonality/{ticker}/')
async def get_seasonality(ticker: str, start: int=default_start, end: int=default_end):

    ticker = change_ticker(ticker)
    
    start_date = str(start) + '-01-01'
    end_date = str(end) + '-01-01'

    df = download_td_test(start_date=start_date, end_date=end_date, ticker=ticker)
    df1 = manage_seasonality(df)
    df2 = calculate_seasonality(df1)
    finale = return_json_format(df2)


    return finale


@app.get('/get-seasonality/{ticker}/history/')
async def get_seasonality(ticker: str, start: int=default_start, end: int=default_end):

    ticker = change_ticker(ticker)
    df = plot_single_year(ticker=ticker, start=start, end=end)
    return df


@app.get('/get-seasonality/{ticker}/monthly/')
async def get_monthly_returns(ticker: str, start: int=default_start, end: int=default_end):
    startend = int(str(start) + str(end))
    data = monthly_returns(ticker = ticker, startend=startend)
    return data


@app.get('/get-seasonality/{ticker}/stdev/')
async def get_monthly_returns(ticker: str, start: int=default_start, end: int=default_end):
    startend = int(str(start) + str(end))
    data = monthly_stdev(ticker = ticker, startend=startend)
    return data
    
