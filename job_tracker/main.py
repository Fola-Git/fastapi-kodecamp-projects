from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List
from file_handler import load_data, save_data

app = FastAPI()

class JobApplication(BaseModel):
    name: str
    company: str
    position: str
    status: str  # pending, accepted, interview, rejected

@app.post("/applications/")
def add_application(app_data: JobApplication):
    try:
        data = load_data()
        data.append(app_data.dict())
        save_data(data)
        return {"message": "Application added", "data": app_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/applications/", response_model=List[JobApplication])
def get_all_applications():
    return load_data()

@app.get("/applications/search")
def search_by_status(status: str = Query(...)):
    try:
        data = load_data()
        filtered = [app for app in data if app["status"].lower() == status.lower()]
        return filtered
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
