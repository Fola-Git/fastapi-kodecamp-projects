from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()

# In-memory contact list
contacts = {}

class Contact(BaseModel):
    name: str
    phone: str
    email: str

@app.post("/contacts/")
def add_contact(contact: Contact):
    if contact.name in contacts:
        raise HTTPException(status_code=400, detail="Contact already exists.")
    contacts[contact.name] = contact.dict()
    return {"message": "Contact added", "contact": contact}

@app.get("/contacts/")
def get_contact(name: str = Query(...)):
    contact = contacts.get(name)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found.")
    return contact

@app.put("/contacts/{name}")
def update_contact(name: str, updated: Contact):
    if name not in contacts:
        raise HTTPException(status_code=404, detail="Contact not found.")
    contacts[name] = updated.dict()
    return {"message": "Contact updated", "contact": updated}

@app.delete("/contacts/{name}")
def delete_contact(name: str):
    if name not in contacts:
        raise HTTPException(status_code=404, detail="Contact not found.")
    del contacts[name]
    return {"message": f"Contact '{name}' deleted."}
