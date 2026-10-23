import json
from fastapi import FastAPI, Path, HTTPException, Query


app = FastAPI()
with open("student.json", "r") as file:
    student = json.load(file)





@app.get("/")
def Home():
    return{
        "Message":"Welcome To Student Management API"
    }
    

@app.get("/About")
def About():
    return {
        "About":"This Is Fully Functional Student Management API"
    }
    


@app.get("/View")
def View():
    return student



@app.get("/student/{student_id}")
def View_student(student_id: int = Path(description="Enter The Student ID",example=101)):
    
    for std in student:
        
        if std["id"] == student_id:
            return std
    raise HTTPException(status_code=404, detail="Student Not Found")





@app.get("/students/course/{course_name}")
def filter_students(
    course_name: str,
    min_marks: int = Query(0, description="Minimum marks"),
    city: str | None = Query(None, description="Filter by city")
):
    valid_students = []

    for s in student:

        if s["course"].lower() == course_name.lower():

            if s["marks"] >= min_marks:

                if city is None or s["city"].lower() == city.lower():

                    valid_students.append(s)

    return valid_students

