# Task 7 – Notes API

- SQLModel Note model
- Middleware counts requests and logs them; header `X-Total-Requests`
- Backup all notes to `notes.json` after create/delete
- CORS for localhost:3000 and 127.0.0.1:5500

## Run
```bash
cd task7_notes_api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
