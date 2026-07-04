from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time
import uuid


app = FastAPI()


# Your assigned origin
allowed_origin = "https://dash-im95k4.example.com"


# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[allowed_origin],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


# Custom middleware for required headers
class MetricsMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        response.headers["X-Request-ID"] = str(uuid.uuid4())
        response.headers["X-Process-Time"] = str(process_time)

        return response


app.add_middleware(MetricsMiddleware)


@app.get("/stats")
def stats(values: str = Query(...)):

    nums = [int(x) for x in values.split(",")]

    return {
        "email": "25f2008314@ds.study.iitm.ac.in",
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / len(nums)
    }
