from fastapi import FastAPI, Path, Request
from pydantic import BaseModel
from typing import Optional
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from helpers_seasonality import *

from helpers_seasonality import *



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/node_modules", StaticFiles(directory="node_modules"), name="node_modules")

app.add_middleware(GZipMiddleware)

templates = Jinja2Templates(directory="templates")


def change_ticker(ticker):
    commodities = ['XAU', 'XG', 'XBR', 'XPT']
    
    if ticker in commodities:
        return ticker + "/USD"
    else:
        return ticker


default_start = 2012
default_end = 2022


@app.get("/")
async def landing(request: Request):
    context = {}
    return templates.TemplateResponse(name="landing.html", request=request, context = context)

@app.get("/educational")
async def educational(request: Request):
    context = {}
    return templates.TemplateResponse(name="educational.html", request=request, context = context)

@app.get("/about")
async def about(request: Request):
    context = {}
    return templates.TemplateResponse(name="about.html", request=request, context = context)



@app.get("/{ticker}")
async def index(request: Request, ticker: str, start: int=default_start, end: int=default_end):
    context = {
        "ticker": ticker,
        "start": start,
        "end": end,
    }
    return templates.TemplateResponse(name="base.html", request=request, context = context)



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


@app.get('/get-seasonality/{ticker}/history')
async def get_seasonality(ticker: str, start: int=default_start, end: int=default_end):

    ticker = change_ticker(ticker)
    
    print("fastapi", start,end)
    
    df = plot_single_year(start, end, ticker)
    return df


@app.get('/get-seasonality/{ticker}/monthly')
async def get_monthly_returns(ticker: str, start: int=default_start, end: int=default_end):
    startend = int(str(start) + str(end))
    data = monthly_returns(ticker = ticker, startend=startend)
    return data


@app.get('/get-seasonality/{ticker}/stdev')
async def get_monthly_returns(ticker: str, start: int=default_start, end: int=default_end):
    startend = int(str(start) + str(end))
    data = monthly_stdev(ticker = ticker, startend=startend)
    return data
    
