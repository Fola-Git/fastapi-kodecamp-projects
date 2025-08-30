from fastapi import Request
import threading

class RequestCounter:
    def __init__(self):
        self.total = 0
        self.lock = threading.Lock()

def add_counter(app, logfile: str = "requests.log"):
    counter = RequestCounter()
    app.state.request_counter = counter

    @app.middleware("http")
    async def count_requests(request: Request, call_next):
        with counter.lock:
            counter.total += 1
            current = counter.total
        response = await call_next(request)
        with open(logfile, "a") as f:
            f.write(f"Total so far: {current}\n")
        response.headers["X-Total-Requests"] = str(current)
        return response
