from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlmodel import select
from .database import init_db, get_session
from .models import Contact, User
from .security import current_user, hash_pw, verify_pw, token_for
from .middleware import log_ip
from .cors import add_cors

app = FastAPI(title="Contacts API")
add_cors(app)
log_ip(app)

@app.on_event("startup")
def on_startup():
    init_db()

from fastapi.security import OAuth2PasswordRequestForm

@app.post("/register")
def register(username: str, password: str, session=Depends(get_session)):
    if session.exec(select(User).where(User.username==username)).first():
        raise HTTPException(400, "Username exists")
    u = User(username=username, hashed_password=hash_pw(password))
    session.add(u); session.commit()
    return {"ok": True}

@app.post("/token")
def token(form: OAuth2PasswordRequestForm = Depends(), session=Depends(get_session)):
    u = session.exec(select(User).where(User.username==form.username)).first()
    if not u or not verify_pw(form.password, u.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": token_for(u.username), "token_type":"bearer"}

@app.post("/contacts/", response_model=Contact)
def add_contact(contact: Contact, user: User = Depends(current_user), session=Depends(get_session)):
    contact.user_id = user.id
    session.add(contact); session.commit(); session.refresh(contact)
    return contact

@app.get("/contacts/", response_model=List[Contact])
def list_contacts(user: User = Depends(current_user), session=Depends(get_session)):
    return session.exec(select(Contact).where(Contact.user_id==user.id)).all()

@app.put("/contacts/{contact_id}", response_model=Contact)
def update_contact(contact_id: int, update: Contact, user: User = Depends(current_user), session=Depends(get_session)):
    c = session.get(Contact, contact_id)
    if not c or c.user_id != user.id: raise HTTPException(404, "Not found")
    c.name, c.email, c.phone = update.name, update.email, update.phone
    session.add(c); session.commit(); session.refresh(c)
    return c

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, user: User = Depends(current_user), session=Depends(get_session)):
    c = session.get(Contact, contact_id)
    if not c or c.user_id != user.id: raise HTTPException(404, "Not found")
    session.delete(c); session.commit()
    return {"ok": True}
