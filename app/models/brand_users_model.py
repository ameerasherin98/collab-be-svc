from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class BrandUser(Base):
    __tablename__ = "brand_users"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    profile_picture = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
