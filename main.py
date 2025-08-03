from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

# --- Models ---
class Student(BaseModel):
    name: str
    subject_scores: dict

# --- Helpers ---
def calculate_average(scores):
    return sum(scores.values()) / len(scores)

def calculate_grade(avg):
    if avg >= 70:
        return "A"
    elif avg >= 60:
        return "B"
    elif avg >= 50:
        return "C"
    elif avg >= 40:
        return "D"
    else:
        return "F"

def load_students():
    try:
        with open("students.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_students(students):
    try:
        with open("students.json", "w") as f:
            json.dump(students, f, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Endpoints ---
@app.post("/students/")
def add_student(student: Student):
    students = load_students()
    average = calculate_average(student.subject_scores)
    grade = calculate_grade(average)

    student_data = {
        "name": student.name,
        "subject_scores": student.subject_scores,
        "average": round(average, 2),
        "grade": grade
    }

    students.append(student_data)
    save_students(students)

    return student_data

@app.get("/students/")
def get_all_students():
    return load_students()

@app.get("/students/{name}")
def get_student(name: str):
    students = load_students()
    for student in students:
        if student["name"].lower() == name.lower():
            return student
    raise HTTPException(status_code=404, detail="Student not found")
