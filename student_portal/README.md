# Student Portal API — My Implementation

I built a simple API for students to register, log in, and check their grades. I used HTTP Basic authentication for security.

## How I Set It Up

- Registration (`POST /register/`): Adds new students to `students.json` with hashed passwords.
- Login (`POST /login/`): Authenticates users.
- Grades (`GET /grades/`): Protected endpoint; only logged-in students can see their grades.

## Steps to Run

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Then, open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test the API.