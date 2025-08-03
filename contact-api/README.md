# contact-api

A FastAPI service for managing contacts.

## Endpoints

- `POST /contacts/` — Add a new contact.
- `GET /contacts/?name=<name>` — Get a contact by name.
- `PUT /contacts/{name}` — Update a contact.
- `DELETE /contacts/{name}` — Delete a contact.

## Usage

Start the API:
```sh
uvicorn main:app --reload
```