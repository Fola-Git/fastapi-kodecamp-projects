from typing import Optional, List
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    hashed_password: str

class JobApplication(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    company: str
    position: str
    status: str  # pending, interviewing, rejected, accepted
    date_applied: str
    user_id: int = Field(foreign_key="user.id")
