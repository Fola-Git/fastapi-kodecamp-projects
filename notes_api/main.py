from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

NOTES_DIR = "notes"

if not os.path.exists(NOTES_DIR):
    os.makedirs(NOTES_DIR)

class Note(BaseModel):
    title: str
    content: str

@app.post("/notes/")
def create_note(note: Note):
    filename = os.path.join(NOTES_DIR, f"{note.title}.txt")
    if os.path.exists(filename):
        raise HTTPException(status_code=400, detail="Note already exists.")
    try:
        with open(filename, "w") as f:
            f.write(note.content)
        return {"message": "Note created."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/notes/{title}")
def get_note(title: str):
    filename = os.path.join(NOTES_DIR, f"{title}.txt")
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="Note not found.")
    try:
        with open(filename, "r") as f:
            content = f.read()
        return {"title": title, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/notes/{title}")
def update_note(title: str, updated: Note):
    filename = os.path.join(NOTES_DIR, f"{title}.txt")
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="Note not found.")
    try:
        with open(filename, "w") as f:
            f.write(updated.content)
        return {"message": "Note updated."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/notes/{title}")
def delete_note(title: str):
    filename = os.path.join(NOTES_DIR, f"{title}.txt")
    if not os.path.exists(filename):
        raise HTTPException(status_code=404, detail="Note not found.")
    try:
        os.remove(filename)
        return {"message": "Note deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
