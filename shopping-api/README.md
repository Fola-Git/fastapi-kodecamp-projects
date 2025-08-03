# shopping-api

A FastAPI service for shopping cart management.

## Endpoints

- `GET /products/` — List products.
- `POST /cart/add?product_id=<id>&qty=<qty>` — Add item to cart.
- `GET /cart/checkout` — Checkout cart.

## Usage

Start the API:
```sh
uvicorn main:app --reload
```