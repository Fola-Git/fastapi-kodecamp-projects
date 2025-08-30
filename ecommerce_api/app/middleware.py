import time
from fastapi import Request

def add_timing_header(app):
    @app.middleware("http")
    async def add_process_time(request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        response.headers["X-Process-Time-ms"] = f"{(time.time()-start)*1000:.2f}"
        return response
