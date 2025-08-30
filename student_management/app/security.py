import json, base64
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pathlib import Path

security = HTTPBasic()
USERS_FILE = Path(__file__).resolve().parent.parent / "users.json"

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    if not USERS_FILE.exists():
        raise HTTPException(status_code=500, detail="users.json not found")
    users = json.loads(USERS_FILE.read_text())
    username = credentials.username
    password = credentials.password
    if username in users and users[username] == password:
        return username
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate":"Basic"})
