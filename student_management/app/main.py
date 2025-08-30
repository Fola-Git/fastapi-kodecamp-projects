from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlmodel import select
from .database import init_db, get_session
from .models import Student, StudentCreate, StudentRead, StudentUpdate, Grade
from .security import get_current_user
from .cors import add_cors
from .logging_mw import add_request_logger

app = FastAPI(title="Student Management System")
add_cors(app)
add_request_logger(app)

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/students/", response_model=List[StudentRead])
def list_students(session=Depends(get_session)):
    result = session.exec(select(Student)).all()
    return result

@app.post("/students/", response_model=StudentRead)
def create_student(payload: StudentCreate, user: str = Depends(get_current_user), session=Depends(get_session)):
    student = Student(name=payload.name, age=payload.age, email=payload.email)
    session.add(student)
    session.commit()
    session.refresh(student)
    if payload.grades:
        for g in payload.grades:
            grade = Grade(subject=g["subject"], score=g["score"], student_id=student.id)
            session.add(grade)
        session.commit()
        session.refresh(student)
    return student

@app.get("/students/{student_id}", response_model=StudentRead)
def get_student(student_id: int, session=Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    return student

@app.patch("/students/{student_id}", response_model=StudentRead)
def update_student(student_id: int, payload: StudentUpdate, user: str = Depends(get_current_user), session=Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(student, k, v)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@app.delete("/students/{student_id}")
def delete_student(student_id: int, user: str = Depends(get_current_user), session=Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(404, "Student not found")
    session.delete(student)
    session.commit()
    return {"ok": True}
