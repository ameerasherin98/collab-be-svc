import uuid

from pydantic import BaseModel, EmailStr

class BrandUserSchema(BaseModel):
    user_id: uuid.UUID
    google_id: str
    name: str
    email: EmailStr
    profile_picture: str | None = None  # Optional field

    class Config:
        from_attributes = True  # Enables conversion from ORM model
