from sqlalchemy.orm import Session
import uuid
from app.models.campaign import Campaign

def get_campaign_by_id(db: Session, campaign_id: uuid.UUID) -> Campaign:
    return db.query(Campaign).filter(Campaign.campaign_id == campaign_id).first()

def create_campaign(db: Session, campaign: Campaign) -> Campaign:
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign

def update_campaign(db: Session, campaign: Campaign, campaign_data: dict) -> Campaign:
    for field, value in campaign_data.items():
        setattr(campaign, field, value)
    db.commit()
    db.refresh(campaign)
    return campaign

def delete_campaign(db: Session, campaign: Campaign):
    db.delete(campaign)
    db.commit()
