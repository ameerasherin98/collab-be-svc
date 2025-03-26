import os
import datetime

from authlib.jose import jwt
from fastapi import HTTPException
from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from starlette.requests import Request
from dotenv import load_dotenv
from starlette.responses import JSONResponse

from app.repositories.user_repository import get_or_create_brand_user

load_dotenv()

# JWT Secret and Algorithm
JWT_SECRET = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"

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

def create_jwt(user):
    """Generate a JWT token for the authenticated user."""
    now = datetime.datetime.now()
    payload = {
        "sub": user.google_id,
        "email": user.email,
        "exp": now + datetime.timedelta(days=3),  # 7-day expiration
        "iat": now
    }
    header = {"alg": JWT_ALGORITHM}
    return jwt.encode(header, payload, JWT_SECRET)

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

        # Generate JWT Token
        access_token = create_jwt(user)
        response = JSONResponse(content={"message": "Login successful"})
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,  # Prevents JS access (XSS protection)
            secure=True,  # Use True in production (requires HTTPS)
            max_age=3 * 24 * 60 * 60,  # 7 days expiration
        )

        return response

    except Exception as e:
        print("ERROR:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
