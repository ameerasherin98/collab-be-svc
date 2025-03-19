from sqlalchemy.orm import Session

from app.models.brand_users_model import BrandUser

def get_brand_user_by_google_id(db: Session, google_id: str):
    return db.query(BrandUser).filter(BrandUser.google_id.__eq__(google_id)).first()

def create_brand_user(db: Session, user_data: dict):
    db_user = BrandUser(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
