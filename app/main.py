import os

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.api.auth.brand_auth import brand_auth_router
from app.api.campaign.campaign import campaign_router
from app.database import create_tables
from app.middlewear.auth_middleware import JWTMiddleware

load_dotenv()

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Hello, World!"}


create_tables()

SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "supersecretkey")

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY
)
# app.add_middleware(JWTMiddleware)
app.include_router(brand_auth_router, prefix="/auth")
app.include_router(campaign_router, prefix="/campaigns")

