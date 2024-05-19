from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Optional
import json

from helpers_seasonality import *

app = FastAPI()

@app.get('/')
async def hello_world():
    return {"Msg": "Hello World!"}


@app.get('/get-seasonality/{ticker}/{startend}')
async def get_seasonality(startend: int, ticker: str):

    string = str(startend)

    start = string[:4]
    end = string[4:]

    ticker = ticker + '/USD'

    start_date = start + '-01-01'
    end_date = end + '-01-01'

    df = download_td_test(start_date = start, end_date = end, ticker = ticker)
    df1 = manage_seasonality(df)
    df2 = calculate_seasonality(df1)
    finale = return_json_format(df2)


    return finale


@app.get('/get-seasonality/{ticker}/{startend}/history')
async def get_seasonality(startend: int, ticker: str):
    ticker = ticker + '/USD'

    variabile = plot_single_year(startend = startend, ticker = ticker)
    return json.dumps(variabile)









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