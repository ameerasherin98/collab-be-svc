from authlib.jose import jwt
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import os

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """Extract JWT from cookies and attach user info to request state."""
        token = request.cookies.get("access_token")

        if token:
            try:
                payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
                request.state.user = payload  # Attach user info to request
            except jwt.ExpiredSignatureError:
                raise HTTPException(status_code=401, detail="Token expired")
            except jwt.InvalidTokenError:
                raise HTTPException(status_code=401, detail="Invalid token")

        response = await call_next(request)
        return response
