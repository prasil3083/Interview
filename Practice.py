from fastapi import FastAPI , Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

students = {
    1 : {"name" : "John",
         "age" : 17,
         "class" : "Year 12"}
}

class Student(BaseModel):
    name : str
    age : int
    year : str

class UpdateStudent(BaseModel):
    name : Optional[str] = None
    age : Optional[int]= None
    year : Optional[str] = None

@app.get("/")
def index():
    return {"name" : "stefan Alexus"}

@app.get("/get-student/{student_id}")
def def_student(student_id : int = Path(... , description = "enter the student id", gt = 0)):
    return students[student_id]

@app.get("/get-by-name")
def get_student(* ,name : Optional[str] = None ,test : int ):
    for student_id in students:
        if students[student_id]["name"] == name :
            return students[student_id]
        
    return {"data" :" Not found"}

@app.post("/creat-student/{student_id}")
def create_student(student_id : int, student : Student ):
    if student_id in students :
        return {"error" : "Student exist"}
    
    students[student_id] = student
    return students[student_id]

@app.put("/update-student/{studen_id}")
def update_student(student_id :int, student : UpdateStudent):
    if student_id not in students:
        return { "error" : "Student Does not exist"}

    if student.name != None:
        students[student_id].name = student.name
    if student.age != None:
        students[student_id].age = student.age
    if student.year != None:
        students[student_id].year = student.year

    return students[student_id]
