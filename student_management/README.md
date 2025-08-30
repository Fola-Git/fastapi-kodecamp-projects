# Task 1 – Student Management System

Auth: **HTTP Basic** using `users.json`. Only logged-in users can create/update/delete.

## Run
```bash
cd student_management
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
Swagger: http://127.0.0.1:8000/docs

## Test auth in curl
```bash
curl -u admin:admin -X POST http://127.0.0.1:8000/students/ -H "Content-Type: application/json" -d '{"name":"Ada","age":20,"email":"ada@example.com","grades":[{"subject":"Math","score":95}] }'
```
