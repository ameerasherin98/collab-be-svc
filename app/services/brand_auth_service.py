import os
from fastapi import HTTPException
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from starlette.requests import Request
from dotenv import load_dotenv

from app.repositories.user_repository import get_or_create_brand_user

load_dotenv()

# Initialize OAuth
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

async def handle_oauth_callback(request: Request, db: Session):
    """Process the OAuth callback, validate state, and create a user."""
    try:
        stored_state = request.session.get("oauth_state")  # Retrieve stored state
        received_state = request.query_params.get("state")  # Get state from URL

        if stored_state is None:
            raise HTTPException(status_code=400, detail="Missing stored state. Possible session issue.")

        if stored_state != received_state:
            raise HTTPException(status_code=400, detail="CSRF Warning! State does not match.")

        # Exchange the code for a token
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get("userinfo")

        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to retrieve user info.")

        user = get_or_create_brand_user(
            db=db,
            google_id=user_info["sub"],
            name=user_info["name"],
            email=user_info["email"],
            profile_picture=user_info.get("picture", ""),
        )

        return {"message": "Login successful", "user": user}

    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
