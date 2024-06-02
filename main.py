from fastapi import FastAPI, Path, Request
from pydantic import BaseModel
from typing import Optional
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from helpers_seasonality import *



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/node_modules", StaticFiles(directory="node_modules"), name="node_modules")
app.add_middleware(GZipMiddleware)
templates = Jinja2Templates(directory="templates")



def change_ticker(ticker):
    #TODO: Generalize it more
    """
    Modifies the ticker symbol for specific commodities.

    Args:
    ticker (str): The ticker symbol to modify.

    Returns:
    str: The modified ticker symbol.
    """
    commodities = ['XAU', 'XG', 'XBR', 'XPT']
    
    if ticker in commodities:
        return ticker + "/USD"
    else:
        return ticker


default_start = 2012
default_end = 2022



@app.get("/")
async def landing(request: Request):
    """
    Renders the landing page, redirecting you to landing.html.
    """
    context = {}
    return templates.TemplateResponse(name="landing.html", request=request, context = context)



@app.get("/educational")
async def educational(request: Request):
    """
    Handles GET requests to the /educational endpoint and returns the educational.html template.
    """
    context = {}
    return templates.TemplateResponse(name="educational.html", request=request, context = context)



@app.get("/about")
async def about(request: Request):
    """
    Handles GET requests to the /about endpoint and returns the about.html template.
    """
    context = {}
    return templates.TemplateResponse(name="about.html", request=request, context = context)



@app.get("/{ticker}")
async def index(request: Request, ticker: str, start: int=default_start, end: int=default_end):
    """
    Renders the page base.html showing the charts for of that ticker.
    Args:
    ticker (str): The ticker symbol.
    start (int, optional): The start year. Defaults to 2012.
    end (int, optional): The end year. Defaults to 2022.
    """
    context = {
        "ticker": ticker,
        "start": start,
        "end": end,
    }
    return templates.TemplateResponse(name="base.html", request=request, context=context)



@app.get('/get-seasonality/{ticker}/')
async def get_seasonality(ticker: str, start: int=default_start, end: int=default_end):
    """
    This page is fetched when clicking Submit, and returns seasonality data for a given ticker.

    Args:
    ticker (str): The ticker symbol.
    start (int, optional): The start year. Defaults to 2012.
    end (int, optional): The end year. Defaults to 2022.

    Returns:
    dict: The seasonality data in JSON format.
    """

    ticker = change_ticker(ticker)
    start_date = str(start) + '-01-01'
    end_date = str(end) + '-01-01'

    prices = download_td_test(start_date=start_date, end_date=end_date, ticker=ticker)
    _seasonality = manage_seasonality(prices) #The _ stays for 'working with this thing (seasonality)'
    seasonality_df = calculate_seasonality(_seasonality)
    prices_and_timestamps = return_json_format(seasonality_df)


    return prices_and_timestamps


@app.get('/get-seasonality/{ticker}/history')
async def get_seasonality(ticker: str, start: int=default_start, end: int=default_end):
    """
    This page is fetched when clicking Submit, and returns historical seasonality data for a given ticker.

    Args:
    ticker (str): The ticker symbol.
    start (int, optional): The start year. Defaults to 2012.
    end (int, optional): The end year. Defaults to 2022.

    Returns:
    dict: The historical seasonality data.
    """

    ticker = change_ticker(ticker)
    df = plot_single_year(start, end, ticker)

    return df


@app.get('/get-seasonality/{ticker}/monthly')
async def get_monthly_returns(ticker: str, start: int=default_start, end: int=default_end):
    """
    Fetches and returns monthly returns for a given ticker.

    Args:
    ticker (str): The ticker symbol.
    start (int, optional): The start year. Defaults to 2012.
    end (int, optional): The end year. Defaults to 2022.

    Returns:
    dict: The monthly returns data.
    """

    startend = int(str(start) + str(end)) # Example: 2022, 2023 -> 20222023
    data = monthly_returns(ticker = ticker, startend=startend)

    return data


@app.get('/get-seasonality/{ticker}/stdev')
async def get_monthly_returns(ticker: str, start: int=default_start, end: int=default_end):
    """
    Fetches and returns monthly standard deviation for a given ticker.

    Args:
    ticker (str): The ticker symbol.
    start (int, optional): The start year. Defaults to 2012.
    end (int, optional): The end year. Defaults to 2022.

    Returns:
    dict: The monthly standard deviation data.
    """
    startend = int(str(start) + str(end))
    data = monthly_stdev(ticker = ticker, startend=startend)

    return data