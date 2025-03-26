from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.schemas.campaign import CampaignResponse, CampaignCreate
from app.repositories.campaign_repository import get_campaign_by_id, create_campaign, update_campaign, delete_campaign
from app.services.campaign_service import create_campaign_entity, map_campaign_to_response

campaign_router = APIRouter()

@campaign_router.post("/", response_model=CampaignResponse)
def create_campaign_endpoint(campaign_data: CampaignCreate, db: Session = Depends(get_db)):
    campaign = create_campaign_entity(campaign_data)
    campaign = create_campaign(db, campaign)
    return map_campaign_to_response(campaign)

@campaign_router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign_endpoint(campaign_id: uuid.UUID, db: Session = Depends(get_db)):
    campaign = get_campaign_by_id(db, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return map_campaign_to_response(campaign)

@campaign_router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign_endpoint(campaign_id: uuid.UUID, campaign_data: CampaignCreate, db: Session = Depends(get_db)):
    campaign = get_campaign_by_id(db, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    updated_campaign = update_campaign(db, campaign, campaign_data.dict(exclude_unset=True))
    return map_campaign_to_response(updated_campaign)

@campaign_router.delete("/{campaign_id}")
def delete_campaign_endpoint(campaign_id: uuid.UUID, db: Session = Depends(get_db)):
    campaign = get_campaign_by_id(db, campaign_id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    delete_campaign(db, campaign)
    return {"detail": "Campaign deleted successfully"}
