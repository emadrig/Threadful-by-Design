from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import accounts
import os

app = FastAPI()
app.include_router(accounts.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        os.environ.get("CORS_HOST", "http://localhost:3000")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/launch-details")
def launch_details():
    return {
        "launch_details": {
            "year": 2023,
            "month": 2,
            "day": "13",
            "hour": 23,
            "min": 0,
            "tz:": "PST"
        }
    }
