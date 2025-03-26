from authlib.jose import jwt
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import os

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"

EXCLUDED_PATHS = {"/auth/login", "/auth/callback"}  # Allow public access


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """Extract JWT from cookies and attach user info to request state."""

        # Skip middleware for login and callback routes
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)

        token = request.cookies.get("access_token")

        if not token:
            return JSONResponse(status_code=401, content={"detail": "Authentication required"})

        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            request.state.user = payload  # Attach user info to request
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "Token expired"})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        return await call_next(request)
