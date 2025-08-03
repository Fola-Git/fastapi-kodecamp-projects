# notes_api

A FastAPI service for managing notes.

## Endpoints

- `POST /notes/` — Create a note.
- `GET /notes/{title}` — Get a note by title.
- `PUT /notes/{title}` — Update a note.
- `DELETE /notes/{title}` — Delete a note.

## Usage

Start the API:
```sh
uvicorn main:app --reload
```