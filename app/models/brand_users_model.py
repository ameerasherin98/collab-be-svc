import uuid

from sqlalchemy import Column, String, Boolean, UUID

from app.database import Base


class BrandUser(Base):
    __tablename__ = "brand_users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    google_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    profile_picture = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
