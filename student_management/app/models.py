
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    email: str
    grades: List["Grade"] = Relationship(back_populates="student")

class Grade(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subject: str
    score: float
    student_id: int = Field(default=None, foreign_key="student.id")
    student: Optional[Student] = Relationship(back_populates="grades")

class StudentCreate(SQLModel):
    name: str
    age: int
    email: str
    grades: Optional[List[dict]] = None  # list of {{subject, score}}

class StudentRead(SQLModel):
    id: int
    name: str
    age: int
    email: str
    grades: List["Grade"] = []

class StudentUpdate(SQLModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[str] = None
