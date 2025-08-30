from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlmodel import Session, select
from .models import User
from .database import get_session

SECRET="changeme-contacts"
ALGO="HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_pw(p): return pwd.hash(p)
def verify_pw(p,h): return pwd.verify(p,h)

def token_for(username: str):
    return jwt.encode({"sub": username, "exp": datetime.utcnow()+timedelta(hours=2)}, SECRET, algorithm=ALGO)

def current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        sub = payload.get("sub")
    except JWTError:
        raise HTTPException(401, "Invalid token")
    user = session.exec(select(User).where(User.username==sub)).first()
    if not user:
        raise HTTPException(401, "User not found")
    return user
