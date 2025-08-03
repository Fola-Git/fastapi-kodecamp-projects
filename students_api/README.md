# students_api

A FastAPI service for managing student records.

## Endpoints

- `POST /students/` — Add a student.
- `GET /students/` — List all students.
- `GET /students/{name}` — Get student by name.

## Usage

Start the API:
```sh
uvicorn main:app