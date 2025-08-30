from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlmodel import select
from .database import init_db, get_session
from .models import Note
from .middleware import add_counter
from .backup import backup_all
from .cors import add_cors

app = FastAPI(title="Notes API")
add_cors(app)
add_counter(app)

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/notes/", response_model=Note)
def create_note(note: Note, session=Depends(get_session)):
    session.add(note); session.commit(); session.refresh(note)
    notes = session.exec(select(Note)).all()
    backup_all(notes)
    return note

@app.get("/notes/", response_model=List[Note])
def list_notes(session=Depends(get_session)):
    return session.exec(select(Note)).all()

@app.get("/notes/{note_id}", response_model=Note)
def get_note(note_id: int, session=Depends(get_session)):
    note = session.get(Note, note_id)
    if not note: raise HTTPException(404, "Not found")
    return note

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, session=Depends(get_session)):
    note = session.get(Note, note_id)
    if not note: raise HTTPException(404, "Not found")
    session.delete(note); session.commit()
    notes = session.exec(select(Note)).all()
    backup_all(notes)
    return {"ok": True}
