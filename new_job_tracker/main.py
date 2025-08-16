from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from typing import Dict, List
import json, os
from datetime import date

app = FastAPI(title="Job Application Tracker")

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

USERS_FILE = "users.json"
APPS_FILE = "applications.json"

class User(BaseModel):
    username: str
    password_hash: str

class JobApplication(BaseModel):
    job_title: str = Field(..., min_length=2)
    company: str = Field(..., min_length=2)
    date_applied: str = Field(default_factory=lambda: date.today().isoformat())
    status: str = Field(default="applied")

def read_json(path: str, default):
    if not os.path.exists(path):
        try:
            with open(path, "w") as f:
                json.dump(default, f, indent=2)
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"Init {path} error: {e}")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail=f"Read {path} error: {e}")


def write_json(path: str, payload):
    try:
        with open(path, "w") as f:
            json.dump(payload, f, indent=2)
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Write {path} error: {e}")

def read_users() -> Dict[str, User]:
    data = read_json(USERS_FILE, {
        "sam": {"username": "sam", "password_hash": pwd_context.hash("sam123")},
        "tola": {"username": "tola", "password_hash": pwd_context.hash("tola123")},
    })
    return {k: User(**v) for k, v in data.items()}

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> User:
    users = read_users()
    user = users.get(credentials.username)
    if not user or not pwd_context.verify(credentials.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

@app.post("/applications/")
def add_application(app_req: JobApplication, user: User = Depends(get_current_user)):
    data = read_json(APPS_FILE, {})
    user_apps: List[dict] = data.get(user.username, [])
    user_apps.append(app_req.model_dump())
    data[user.username] = user_apps
    write_json(APPS_FILE, data)
    return {"message": "Application added", "application": app_req}

@app.get("/applications/")
def list_applications(user: User = Depends(get_current_user)):
    data = read_json(APPS_FILE, {})
    return {"username": user.username, "applications": data.get(user.username, [])}