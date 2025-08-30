# Task 5 – Contact Manager API

- JWT auth
- Contact model with `user_id` FK
- IP logging middleware (writes to `ips.log`)
- CORS enabled

## Run
```bash
cd task5_contacts_api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
