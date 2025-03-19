import secrets

from fastapi import APIRouter, HTTPException
from authlib.integrations.starlette_client import OAuth
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
import os
from dotenv import load_dotenv

from app.database import get_db
from app.repositories.user_repository import get_or_create_brand_user

load_dotenv()

brand_auth_router = APIRouter()

# Configure OAuth
oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={
        "response_type": "code",
        "scope": "openid email profile",
        "prompt": "consent",  # Ensures consent is always asked
        "access_type": "offline",  # Ensures a refresh token is issued
    },
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params={
        "grant_type": "authorization_code"
    },
    redirect_uri=os.getenv("GOOGLE_REDIRECT_URI"),
    client_kwargs={"scope": "openid email profile"},
)

@brand_auth_router.get("/login")
async def login(request: Request):
    """Redirect user to Google login page"""
    state = secrets.token_urlsafe(16)  # Generate a secure random state
    request.session["oauth_state"] = state  # Store state in session
    return await oauth.google.authorize_redirect(request, os.getenv("GOOGLE_REDIRECT_URI"), state=state, access_type="offline")

@brand_auth_router.get("/callback")
async def auth_callback(request: Request, db:Session = Depends(get_db)):
    """Handle Google OAuth callback"""
    try:
        stored_state = request.session.get("oauth_state")  # Retrieve stored state
        received_state = request.query_params.get("state")  # Get state from URL

        if stored_state is None:
            raise HTTPException(status_code=400, detail="Missing stored state. Possible session issue.")

        if stored_state != received_state:
            raise HTTPException(status_code=400, detail="CSRF Warning! State does not match.")

        # Exchange the code for a token
        token = await oauth.google.authorize_access_token(request)
        user_info = token['userinfo']

        user = get_or_create_brand_user(
            db=db,
            google_id=user_info["sub"],
            name=user_info["name"],
            email=user_info["email"],
            profile_picture=user_info.get("picture", ""),
        )
        db.close()

        return {"message": "Login successful", "user": user}

    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
