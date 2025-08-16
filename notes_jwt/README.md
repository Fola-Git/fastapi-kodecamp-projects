# Task 4: Notes API with JWT Authentication

- `POST /login/` — returns a JWT
- `POST /notes/` — add a note (requires JWT Bearer)
- `GET /notes/` — view own notes

Notes are stored per-user in `notes.json`.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Get Token via Swagger UI

1. `POST /login/` with username & password to get `access_token`.
2. Click **Authorize** in Swagger, paste `Bearer <access_token>`.
3. Call `/notes/` endpoints.