from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from ..models import User
from ..security import create_access_token, hash_password, verify_password
from ..database import get_session

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register")
def register(username: str, password: str, is_admin: bool = False, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.username == username)).first():
        raise HTTPException(400, "Username taken")
    user = User(username=username, hashed_password=hash_password(password), is_admin=is_admin)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"id": user.id, "username": user.username, "is_admin": user.is_admin}

@router.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form.username)).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({"sub": user.username, "is_admin": user.is_admin})
    return {"access_token": token, "token_type": "bearer"}


