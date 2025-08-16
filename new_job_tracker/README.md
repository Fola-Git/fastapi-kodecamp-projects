# Task 3: Job Application Tracker with Secure Access

Each user can only see their own job applications. Uses HTTP Basic auth and filters by the current user.

## Endpoints

- `POST /applications/` — add an application (auth required)
- `GET /applications/` — list your applications (auth required)

Data file: `applications.json` (per-user mapping)

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```