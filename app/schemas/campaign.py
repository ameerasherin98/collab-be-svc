from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class Budget(BaseModel):
    currency: str = Field(..., example="USD")
    total_amount: float = Field(..., example=5000)
    per_influencer: Optional[float] = Field(None, example=200)

class InfluencerCriteria(BaseModel):
    influencer_type: str = Field(..., example="nano, micro, macro")
    category: str = Field(..., example="fashion, beauty, tech")
    followers_min: Optional[int] = Field(None, example=1000)
    followers_max: Optional[int] = Field(None, example=100000)
    engagement_rate_min: Optional[float] = Field(None, example=2.5)
    location: Optional[str] = Field(None, example="India, USA")
    language_preference: Optional[str] = Field(None, example="English, Hindi")

class TargetAudience(BaseModel):
    age_min: Optional[int] = Field(None, example=18)
    age_max: Optional[int] = Field(None, example=35)
    gender: str = Field(default="any", example="male, female, any")  # <-- Fix here
    location: Optional[str] = Field(None, example="Mumbai, Bangalore")
    interests: Optional[str] = Field(None, example="fitness, skincare, gadgets")

class ContentRequirements(BaseModel):
    platforms: str = Field(default="any", example="Instagram, YouTube")
    content_formats: str = Field(..., example="post, reel, video")
    number_of_posts: int = Field(..., example=2)
    hashtags: Optional[str] = Field(None, example="#brandX, #skincare")
    mentions: Optional[str] = Field(None, example="@brandX_official")
    brand_guidelines: Optional[str] = Field(None, example="Avoid negative language")
    approval_required: bool = Field(..., example=True)

class PerformanceMetrics(BaseModel):
    expected_reach: Optional[int] = Field(None, example=500000)
    expected_engagement: Optional[int] = Field(None, example=20000)
    expected_conversions: Optional[int] = Field(None, example=500)
    tracking_links: Optional[str] = Field(None, example="https://brandx.com/campaign")
    promo_codes: Optional[str] = Field(None, example="BRANDX10")

class CampaignCreate(BaseModel):
    brand_id: uuid.UUID
    campaign_name: str
    campaign_description: Optional[str] = None
    campaign_type: str
    start_date: datetime
    end_date: datetime
    budget: Budget
    influencer_criteria: InfluencerCriteria
    target_audience: TargetAudience
    content_requirements: ContentRequirements
    performance_metrics: PerformanceMetrics

class CampaignResponse(CampaignCreate):
    campaign_id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
