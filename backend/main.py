import os

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from api.v1.routes import user_router_v1

load_dotenv()


ALLOW_CREDENTIALS = os.environ.get("ALLOW_CREDENTIALS").lower() == "true"
ALLOW_HEADERS = os.environ.get("ALLOW_HEADERS").split(",")
ALLOWED_METHODS = os.environ.get("ALLOW_METHODS").split(",")
CORS_ORIGINS = os.environ.get("CORS_ORIGINS").split(",")


router_v1 = APIRouter()
router_v1.include_router(user_router_v1, prefix="/users", tags=["users"])

app = FastAPI(title="MEPH Education API", version="1.0", openapi_prefix="/v1")
app.include_router(router_v1, tags=["v1"], prefix="/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("CORS_ORIGINS", default="*"),
    allow_credentials=os.environ.get("ALLOW_CREDENTIALS", default="true"),
    allow_methods=os.environ.get("ALLOW_METHODS", default="*"),
    allow_headers=os.environ.get("ALLOW_HEADERS", default="*"),
)


@app.get("/v1")
def home():
    return {
        "message": "Hi there!!!",
    }
