# fastapi-kodecamp-projects

This repository contains multiple FastAPI microservices for different use cases:

- **contact-api**: Manage contacts with full CRUD operations. Store, retrieve, update, and delete contact information such as names, emails, and phone numbers.
- **job_tracker**: Track job applications and their statuses. Add new applications, list all, and search by status to organize your job hunt.
- **notes_api**: Create, read, update, and delete personal notes. Useful for storing quick thoughts, reminders, or documentation snippets.
- **shopping-api**: Manage a shopping cart and checkout process. Browse products, add items to your cart, and simulate a checkout flow.
- **students_api**: Manage student records and grades. Add new students, list all, and retrieve individual student details for academic tracking.

## Setup

1. Install Python 3.13+ and [FastAPI](https://fastapi.tiangolo.com/).
2. Install dependencies:
   ```sh
   pip install fastapi uvicorn pydantic
   ```
3. Run any API:
   ```sh
   cd <api-folder>
   uvicorn main:app --reload
   ```

## How to run tests

You can run test at `127.0.0.{port no}/docs`