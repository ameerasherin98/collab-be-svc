from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.models.campaign import Campaign, CampaignStatus
from app.schemas.campaign import CampaignResponse, CampaignCreate, Budget, InfluencerCriteria, TargetAudience, \
    ContentRequirements, PerformanceMetrics

campaign_router = APIRouter()

@campaign_router.post("/", response_model=CampaignResponse)
def create_campaign(campaign_data: CampaignCreate, db: Session = Depends(get_db)):
    campaign = Campaign(
        brand_id=campaign_data.brand_id,
        campaign_name=campaign_data.campaign_name,
        campaign_description=campaign_data.campaign_description,
        campaign_type=campaign_data.campaign_type,
        start_date=campaign_data.start_date,
        end_date=campaign_data.end_date,

        budget_currency=campaign_data.budget.currency,
        budget_total_amount=campaign_data.budget.total_amount,
        budget_per_influencer=campaign_data.budget.per_influencer,

        influencer_type=campaign_data.influencer_criteria.influencer_type,
        category=campaign_data.influencer_criteria.category,
        followers_min=campaign_data.influencer_criteria.followers_min,
        followers_max=campaign_data.influencer_criteria.followers_max,
        engagement_rate_min=campaign_data.influencer_criteria.engagement_rate_min,
        location=campaign_data.influencer_criteria.location,
        language_preference=campaign_data.influencer_criteria.language_preference,

        status=CampaignStatus.draft
    )

    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    campaign_response = CampaignResponse(
        campaign_id=campaign.campaign_id,
        brand_id=campaign.brand_id,
        campaign_name=campaign.campaign_name,
        campaign_description=campaign.campaign_description,
        campaign_type=campaign.campaign_type,
        start_date=campaign.start_date,
        end_date=campaign.end_date,
        budget=Budget(
            currency=campaign.budget_currency,
            total_amount=campaign.budget_total_amount,
            per_influencer=campaign.budget_per_influencer,
        ),
        influencer_criteria=InfluencerCriteria(
            influencer_type=campaign.influencer_type,
            category=campaign.category,
            followers_min=campaign.followers_min,
            followers_max=campaign.followers_max,
            engagement_rate_min=campaign.engagement_rate_min,
            location=campaign.location,
        ),
        target_audience=TargetAudience(
            age_min=campaign.target_age_min,
            age_max=campaign.target_age_max,
            gender=campaign.target_gender,
            location=campaign.target_location,
            interests=campaign.target_interests,
        ),
        content_requirements=ContentRequirements(
            platforms=campaign.platforms,
            content_formats=campaign.content_formats,
            number_of_posts=campaign.number_of_posts,
            hashtags=campaign.hashtags,
            mentions=campaign.mentions,
            brand_guidelines=campaign.brand_guidelines,
            approval_required=campaign.approval_required,
        ),
        performance_metrics=PerformanceMetrics(
            expected_reach=campaign.expected_reach,
            expected_engagement=campaign.expected_engagement,
            expected_conversions=campaign.expected_conversions,
            tracking_links=campaign.tracking_links,
            promo_codes=campaign.promo_codes,
        ),
        status=campaign.status,
        created_at=campaign.created_at,
        updated_at=campaign.updated_at,
    )
    return campaign_response


@campaign_router.get("/{campaign_id}", response_model=CampaignResponse)
def get_campaign(campaign_id: uuid.UUID, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.campaign_id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    campaign_response = CampaignResponse(
        campaign_id=campaign.campaign_id,
        brand_id=campaign.brand_id,
        campaign_name=campaign.campaign_name,
        campaign_description=campaign.campaign_description,
        campaign_type=campaign.campaign_type,
        start_date=campaign.start_date,
        end_date=campaign.end_date,
        budget=Budget(
            currency=campaign.budget_currency,
            total_amount=campaign.budget_total_amount,
            per_influencer=campaign.budget_per_influencer,
        ),
        influencer_criteria=InfluencerCriteria(
            influencer_type=campaign.influencer_type,
            category=campaign.category,
            followers_min=campaign.followers_min,
            followers_max=campaign.followers_max,
            engagement_rate_min=campaign.engagement_rate_min,
            location=campaign.location,
        ),
        target_audience=TargetAudience(
            age_min=campaign.target_age_min,
            age_max=campaign.target_age_max,
            gender=campaign.target_gender,
            location=campaign.target_location,
            interests=campaign.target_interests,
        ),
        content_requirements=ContentRequirements(
            platforms=campaign.platforms,
            content_formats=campaign.content_formats,
            number_of_posts=campaign.number_of_posts,
            hashtags=campaign.hashtags,
            mentions=campaign.mentions,
            brand_guidelines=campaign.brand_guidelines,
            approval_required=campaign.approval_required,
        ),
        performance_metrics=PerformanceMetrics(
            expected_reach=campaign.expected_reach,
            expected_engagement=campaign.expected_engagement,
            expected_conversions=campaign.expected_conversions,
            tracking_links=campaign.tracking_links,
            promo_codes=campaign.promo_codes,
        ),
        status=campaign.status,
        created_at=campaign.created_at,
        updated_at=campaign.updated_at,
    )

    return campaign_response



@campaign_router.put("/{campaign_id}", response_model=CampaignResponse)
def update_campaign(campaign_id: uuid.UUID, campaign_data: CampaignCreate, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.campaign_id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    campaign_response = CampaignResponse(
        campaign_id=campaign.campaign_id,
        brand_id=campaign.brand_id,
        campaign_name=campaign.campaign_name,
        campaign_description=campaign.campaign_description,
        campaign_type=campaign.campaign_type,
        start_date=campaign.start_date,
        end_date=campaign.end_date,
        budget=Budget(
            currency=campaign.budget_currency,
            total_amount=campaign.budget_total_amount,
            per_influencer=campaign.budget_per_influencer,
        ),
        influencer_criteria=InfluencerCriteria(
            influencer_type=campaign.influencer_type,
            category=campaign.category,
            followers_min=campaign.followers_min,
            followers_max=campaign.followers_max,
            engagement_rate_min=campaign.engagement_rate_min,
            location=campaign.location,
        ),
        target_audience=TargetAudience(
            age_min=campaign.target_age_min,
            age_max=campaign.target_age_max,
            gender=campaign.target_gender,
            location=campaign.target_location,
            interests=campaign.target_interests,
        ),
        content_requirements=ContentRequirements(
            platforms=campaign.platforms,
            content_formats=campaign.content_formats,
            number_of_posts=campaign.number_of_posts,
            hashtags=campaign.hashtags,
            mentions=campaign.mentions,
            brand_guidelines=campaign.brand_guidelines,
            approval_required=campaign.approval_required,
        ),
        performance_metrics=PerformanceMetrics(
            expected_reach=campaign.expected_reach,
            expected_engagement=campaign.expected_engagement,
            expected_conversions=campaign.expected_conversions,
            tracking_links=campaign.tracking_links,
            promo_codes=campaign.promo_codes,
        ),
        status=campaign.status,
        created_at=campaign.created_at,
        updated_at=campaign.updated_at,
    )

    db.commit()
    db.refresh(campaign)
    return campaign_response


@campaign_router.delete("/{campaign_id}")
def delete_campaign(campaign_id: uuid.UUID, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.campaign_id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    db.delete(campaign)
    db.commit()
    return {"detail": "Campaign deleted successfully"}
