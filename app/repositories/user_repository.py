from sqlalchemy.orm import Session

from app.models.brand_users_model import BrandUser

def get_or_create_brand_user(db: Session, google_id: str, name: str, email: str, profile_picture: str):
    user = db.query(BrandUser).filter(BrandUser.google_id == google_id).first()
    if not user:
        # First-time user, create a new entry
        user = BrandUser(
            google_id=google_id,
            name=name,
            email=email,
            profile_picture=profile_picture,
            is_verified=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    return user
