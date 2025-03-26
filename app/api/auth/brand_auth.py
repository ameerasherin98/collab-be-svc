import secrets
import os
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from dotenv import load_dotenv
from starlette.responses import RedirectResponse

from app.database import get_db
from app.services.brand_auth_service import oauth, handle_oauth_callback

load_dotenv()

brand_auth_router = APIRouter()

@brand_auth_router.get("/login")
async def login(request: Request):
    """Redirect user to Google login page."""
    state = secrets.token_urlsafe(16)  # Generate a secure random state
    request.session["oauth_state"] = state  # Store state in session

    return await oauth.google.authorize_redirect(
        request,
        os.getenv("GOOGLE_REDIRECT_URI"),
        state=state,
        access_type="offline"
    )

@brand_auth_router.get("/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    """Handle Google OAuth callback."""
    response = await handle_oauth_callback(request, db)
    return RedirectResponse("http://localhost:3000/dashboard")
