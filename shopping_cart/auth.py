from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Dict
import json, os

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

USERS_FILE = "users.json"

class User(BaseModel):
    username: str
    password_hash: str
    role: str  # "admin" or "customer"

def read_users() -> Dict[str, User]:
    if not os.path.exists(USERS_FILE):
        default = {
            "admin": {"username": "admin", "password_hash": pwd_context.hash("admin123"), "role": "admin"},
            "alice": {"username": "alice", "password_hash": pwd_context.hash("alice123"), "role": "customer"},
        }
        try:
            with open(USERS_FILE, "w") as f:
                json.dump(default, f, indent=2)
        except OSError as e:
            raise HTTPException(status_code=500, detail=f"Init users file error: {e}")
    try:
        with open(USERS_FILE, "r") as f:
            raw = json.load(f)
            return {k: User(**v) for k, v in raw.items()}
    except (OSError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=500, detail=f"Users file read error: {e}")

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> User:
    users = read_users()
    user = users.get(credentials.username)
    if not user or not pwd_context.verify(credentials.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

def require_role(role: str):
    def _checker(user: User = Depends(get_current_user)) -> User:
        if user.role != role:
            raise HTTPException(status_code=403, detail="Insufficient privileges")
        return user
    return _checker 