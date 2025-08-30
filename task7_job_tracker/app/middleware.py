from fastapi import Request, HTTPException

def require_user_agent(app):
    @app.middleware("http")
    async def check_ua(request: Request, call_next):
        if "user-agent" not in request.headers or not request.headers["user-agent"].strip():
            raise HTTPException(400, "User-Agent header required")
        return await call_next(request)
