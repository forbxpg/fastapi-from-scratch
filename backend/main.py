"""Main application start module."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


import settings
from db.base import Base
from db.db import engine


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)


@app.get("/")
def home():
    return {
        "message": "Hello World!",
    }


Base.metadata.create_all(engine)
