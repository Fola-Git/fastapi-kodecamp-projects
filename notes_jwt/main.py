from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from typing import Dict, List
from datetime import datetime, timedelta, timezone
import os, json, jwt

app = FastAPI(title="Notes API with JWT")

USERS_FILE = "users.json"
NOTES_FILE = "notes.json"

SECRET_KEY = os.environ.get("JWT_SECRET", "dev-secret-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")
http_bearer = HTTPBearer(auto_error=False)

class User(BaseModel):
    username: str
    password_hash: str

class Note(BaseModel):
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    date: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

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
        "admin": {"username": "admin", "password_hash": pwd_context.hash("admin123")},
        "starr": {"username": "starr", "password_hash": pwd_context.hash("starr123")},
    })
    return {k: User(**v) for k, v in data.items()}

def authenticate_user(username: str, password: str) -> User | None:
    users = read_users()
    user = users.get(username)
    if not user or not pwd_context.verify(password, user.password_hash):
        return None
    return user

def create_access_token(subject: str, expires_delta: timedelta | None = None):
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_username(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token decode error")

@app.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    token = create_access_token(subject=user.username)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/notes/")
def add_note(note: Note, username: str = Depends(get_current_username)):
    data = read_json(NOTES_FILE, {})
    user_notes: List[dict] = data.get(username, [])
    user_notes.append(note.model_dump())
    data[username] = user_notes
    write_json(NOTES_FILE, data)
    return {"message": "Note added", "note": note}

@app.get("/notes/")
def list_notes(username: str = Depends(get_current_username)):
    data = read_json(NOTES_FILE, {})
    return {"username": username, "notes": data.get(username, [])}