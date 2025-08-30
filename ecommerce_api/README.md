# E-Commerce API

- Modular routers: `products`, `cart`, `users`
- JWT auth (password hashing with bcrypt)
- Admin-only product creation
- Response-time middleware adds `X-Process-Time-ms`
- Orders backed up to `orders.json`

## Run
```bash
cd ecommerce_api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
## Sample flow
1. Register:
```bash
http :8000/users/register username=admin password=admin is_admin==true
http :8000/users/register username=alice password=alice
```
2. Login:
```bash
http -f :8000/users/token username=admin password=admin
```
3. Create product (use Bearer token from login):
```bash
http POST :8000/admin/products/ "Authorization:Bearer <TOKEN>" name="Laptop" price:=499.99 stock:=10
```
4. Add to cart & checkout as normal user.
