# Task 3 – Job Application Tracker

- Auth required for all app endpoints.
- Each user can only access their own applications.
- `/applications/search?status=pending`
- Middleware rejects requests without `User-Agent` header.

## Run
```bash
cd task3_job_tracker
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
