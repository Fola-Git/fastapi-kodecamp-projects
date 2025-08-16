# Week 6: Secure Shopping Cart API with Admin Access

This guide assumes you're new to the project. Follow these steps to understand, run, and exercise the secure shopping cart API.

### What this project provides (high level)
- Admins can add products.
- Anyone can list/browse products.
- Only authenticated users can add items to their cart.
- Role checks are enforced via dependency helpers in `auth.py`.
- Data is stored in the simple JSON files included in the repo:
    - `users.json` — demo users and their roles (e.g. `"admin"` or `"user"`).
    - `products.json` — product catalog.
    - `cart.json` — per-user cart contents.

### Endpoints and expected access
- POST /admin/add_product/ — Admin only
    - This endpoint should be protected by a dependency that verifies the caller is authenticated and has role `admin`.
    - Example: send an Authorization header with a token that maps to an admin user.

- GET /products/ — Public
    - No auth required. Returns the contents of `products.json`.

- POST /cart/add/ — Authenticated users only
    - Requires authentication, but any non-admin authenticated user should be allowed.
    - The API should record the item in `cart.json` associated with the authenticated user identity.

### How to test (examples)
- Run the app (from repo root):
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    uvicorn main:app --reload
    ```
- Browse products (no auth):
    ```bash
    curl http://127.0.0.1:8000/products/
    ```

- Add product as admin (replace <ADMIN_TOKEN>):
    ```bash
    curl -X POST http://127.0.0.1:8000/admin/add_product/ \
        -H "Authorization: Bearer <ADMIN_TOKEN>" \
        -H "Content-Type: application/json" \
        -d '{"id": 10, "name": "New Item", "price": 9.99}'
    ```

- Add to cart as authenticated user (replace <USER_TOKEN>):
    ```bash
    curl -X POST http://127.0.0.1:8000/cart/add/ \
        -H "Authorization: Bearer <USER_TOKEN>" \
        -H "Content-Type: application/json" \
        -d '{"product_id": 10, "quantity": 1}'
    ```

Notes:
- Where tokens come from depends on your `auth.py` implementation and `users.json`. If the demo uses static tokens in `users.json`, use those; otherwise use whatever login/token endpoint the project provides.
- If you need to modify roles for testing, edit `users.json` and restart the app.
