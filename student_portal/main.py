from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from typing import List, Dict
import json, os

app = FastAPI(title="Student Portal API")

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

DATA_FILE = "students.json"

class Student(BaseModel):
    username: str = Field(..., min_length=3)
    password_hash: str
    grades: List[float] = []


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    grades: List[float] = []


def read_students() -> Dict[str, Student]:
    if not os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump({}, f)
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"File init error: {e}")
    try:
        with open(DATA_FILE, "r") as f:
            raw = json.load(f)
            return {k: Student(**v) for k, v in raw.items()}
    except (OSError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail=f"File read error: {e}")


def write_students(data: Dict[str, Student]):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump({k: s.model_dump() for k, s in data.items()}, f, indent=2)
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"File write error: {e}")


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def get_current_student(credentials: HTTPBasicCredentials = Depends(security)) -> Student:
    students = read_students()
    user = students.get(credentials.username)
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

@app.post("/register/")
def register(req: RegisterRequest):
    students = read_students()
    if req.username in students:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = pwd_context.hash(req.password)
    students[req.username] = Student(username=req.username, password_hash=hashed, grades=req.grades or [])
    write_students(students)
    return {"message": "Registered successfully"}


@app.post("/login/")
def login(credentials: HTTPBasicCredentials = Depends(security)):
    _ = get_current_student(credentials)
    return {"message": "Login successful"}


@app.get("/grades/")
def get_grades(current: Student = Depends(get_current_student)):
    return {"username": current.username, "grades": current.grades} 