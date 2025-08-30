import time
from fastapi import Request

def add_request_logger(app, logfile_path: str = "request.log"):
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = (time.time() - start) * 1000
        with open(logfile_path, "a") as f:
            f.write(f"{request.method} {request.url.path} {response.status_code} {duration:.2f}ms\n")
        return response
