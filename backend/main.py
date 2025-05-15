"""Main application start module."""

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from api.v1.routes import user_router_v1

import settings
from db.base import Base
from db.db import engine


router_v1 = APIRouter()
router_v1.include_router(user_router_v1, prefix="/users", tags=["users"])

app = FastAPI(title="MEPH Education API", version="1.0", openapi_prefix="/v1")
app.include_router(router_v1, tags=["v1"], prefix="/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOW_HEADERS,
)


@app.get("/v1")
def home():
    return {
        "message": "Hi there!!!",
    }


Base.metadata.create_all(engine)
