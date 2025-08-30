from fastapi import FastAPI, Depends, HTTPException, Query
from typing import List, Optional
from sqlmodel import select
from .database import init_db, get_session
from .models import JobApplication, User
from .security import get_current_user, hash_password, verify_password, create_token, oauth2_scheme
from .middleware import require_user_agent

app = FastAPI(title="Job Application Tracker")
require_user_agent(app)

@app.on_event("startup")
def on_startup():
    init_db()

from fastapi.security import OAuth2PasswordRequestForm
@app.post("/register")
def register(username: str, password: str, session=Depends(get_session)):
    if session.exec(select(User).where(User.username==username)).first():
        raise HTTPException(400, "Username exists")
    user = User(username=username, hashed_password=hash_password(password))
    session.add(user); session.commit()
    return {"ok": True}

@app.post("/token")
def token(form: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)):
    user = session.exec(select(User).where(User.username==form.username)).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": create_token(user.username), "token_type":"bearer"}

@app.post("/applications/")
def create_application(apply: JobApplication, user: User = Depends(get_current_user), session=Depends(get_session)):
    # enforce ownership
    apply.user_id = user.id
    allowed = {"pending","interviewing","rejected","accepted"}
    if apply.status not in allowed:
        raise HTTPException(400, f"status must be one of {allowed}")
    session.add(apply); session.commit(); session.refresh(apply)
    return apply

@app.get("/applications/", response_model=List[JobApplication])
def list_applications(user: User = Depends(get_current_user), session=Depends(get_session)):
    return session.exec(select(JobApplication).where(JobApplication.user_id==user.id)).all()

@app.get("/applications/search", response_model=List[JobApplication])
def search_applications(status: str = Query(...), user: User = Depends(get_current_user), session=Depends(get_session)):
    allowed = {"pending","interviewing","rejected","accepted"}
    if status not in allowed:
        raise HTTPException(400, f"Invalid status. Allowed: {allowed}")
    return session.exec(select(JobApplication).where(JobApplication.user_id==user.id, JobApplication.status==status)).all()
