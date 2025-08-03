# job_tracker

Track job applications with FastAPI.

## Endpoints

- `POST /applications/` — Add a job application.
- `GET /applications/` — List all applications.
- `GET /applications/search?status=<status>` — Search applications by status.

## Usage

Start the API:
```sh
uvicorn main:app --reload
```