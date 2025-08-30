from fastapi import Request

def log_ip(app, logfile: str = "ips.log"):
    @app.middleware("http")
    async def logger(request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        with open(logfile, "a") as f:
            f.write(f"{client_ip}\n")
        return await call_next(request)
