from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Optional
import json
from helpers_seasonality import *


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/node_modules", StaticFiles(directory="node_modules"), name="node_modules")

app.add_middleware(GZipMiddleware)

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(name="base-2.html", request=request, context={"stock": "moneymaker"})


############
def change_ticker(ticker):
    commodities = ['XAU', 'XG', 'XBR', 'XPT']
    
    if ticker in commodities:
        return ticker + "/USD"
    else:
        return ticker


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
