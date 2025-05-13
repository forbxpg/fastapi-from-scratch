import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv


load_dotenv()


ALLOW_CREDENTIALS = os.environ.get("ALLOW_CREDENTIALS").lower() == "true"
ALLOW_HEADERS = os.environ.get("ALLOW_HEADERS").split(",")
ALLOWED_METHODS = os.environ.get("ALLOW_METHODS").split(",")
CORS_ORIGINS = os.environ.get("CORS_ORIGINS").split(",")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("CORS_ORIGINS", default="*"),
    allow_credentials=os.environ.get("ALLOW_CREDENTIALS", default="true"),
    allow_methods=os.environ.get("ALLOW_METHODS", default="*"),
    allow_headers=os.environ.get("ALLOW_HEADERS", default="*"),
)


@app.get("/")
def home():
    return {
        "message": "Hello World!",
    }
