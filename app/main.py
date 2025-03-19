import os

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.auth.brand_auth import brand_auth_router

load_dotenv()

app = FastAPI()

SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "supersecretkey")

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY
)
app.include_router(brand_auth_router, prefix="/auth")
