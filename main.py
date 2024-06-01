from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Optional
import json
from fastapi.templating import Jinja2Templates

from helpers_seasonality import *

app = FastAPI()


class Asset(BaseModel):
    ticker: str
    start: int | None = None
    end: int | None = None


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
    startend = str(start) + str(end)
    data = monthly_returns(ticker = ticker, startend=startend)
    return data


@app.get('/get-seasonality/{ticker}/stdev/')
async def get_monthly_returns(ticker: str, start: int=default_start, end: int=default_end):
    startend = str(start) + str(end)
    data = monthly_stdev(ticker = ticker, startend=startend)
    return data



'''
students = {
    1: {
        'name': 'Pierino',
        'age': 1,
        'job': 'SWE'
    },
    2: {
        'name': 'Frank',
        'age': 19,
        'job': 'Manco a broro'
    },
}

class Student(BaseModel):
    name: str
    age: int
    job: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get-student/{student_id}")
def get_student(student_id: int):
    return students[student_id]

    

@app.get("/get-by-name/{student_id}")
def get_by_name(student_id: int, name: Optional[str] = None):
    for student_id in students:
        if students[student_id]["name"] == name:
            return students[student_id]

    return {"Data": "Not Found"}


@app.post("create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error": "già c'è zio pera"}
    
    students[student_id] = student
    return students[student_id]
'''