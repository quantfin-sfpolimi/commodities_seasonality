from fastapi import FastAPI, Path
from pydantic import BaseModel
from typing import Optional

from helpers_seasonality import *

app = FastAPI()


@app.get('/get-year/{startend}')
async def get_year(startend: int):

    string = str(startend)

    start = string[:4]
    end = string[4:]

    download_td_test(start, end)

    return {'Start': start, 'End': end}












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