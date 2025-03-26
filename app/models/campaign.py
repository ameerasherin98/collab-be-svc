from sqlalchemy import Column, String, Integer, Float, Enum, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

from app.database import Base


class CampaignType(str, enum.Enum):
    pre_launch = "pre_launch"
    brand_awareness = "brand_awareness"
    targeted_sales = "targeted_sales"
    engagement_boost = "engagement_boost"
    product_review = "product_review"
    event_promotion = "event_promotion"


class CampaignStatus(str, enum.Enum):
    draft = "draft"
    active = "active"
    completed = "completed"
    paused = "paused"
    cancelled = "cancelled"


class Campaign(Base):
    __tablename__ = "campaigns"

    campaign_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey("brand_users.user_id"), nullable=False)
    campaign_name = Column(String, nullable=False)
    campaign_description = Column(String, nullable=True)
    campaign_type = Column(Enum(CampaignType), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    budget_currency = Column(String, nullable=False)
    budget_total_amount = Column(Float, nullable=False)
    budget_per_influencer = Column(Float, nullable=True)

    influencer_type = Column(String, nullable=False)  # "nano, micro, macro"
    category = Column(String, nullable=False)  # "fashion, beauty, tech"
    followers_min = Column(Integer, nullable=True)
    followers_max = Column(Integer, nullable=True)
    engagement_rate_min = Column(Float, nullable=True)
    location = Column(String, nullable=True)  # Comma-separated values
    language_preference = Column(String, nullable=True)

    target_age_min = Column(Integer, nullable=True)
    target_age_max = Column(Integer, nullable=True)
    target_gender = Column(String, nullable=False, default="any")
    target_location = Column(String, nullable=True)
    target_interests = Column(String, nullable=True)

    platforms = Column(String, nullable=False, default="Instagram")  # "Instagram, YouTube"
    content_formats = Column(String, nullable=False, default="reel")  # "post, reel, video"
    number_of_posts = Column(Integer, nullable=False, default=1)
    hashtags = Column(String, nullable=True)
    mentions = Column(String, nullable=True)
    brand_guidelines = Column(String, nullable=True)
    approval_required = Column(Boolean, default=True)

    expected_reach = Column(Integer, nullable=True)
    expected_engagement = Column(Integer, nullable=True)
    expected_conversions = Column(Integer, nullable=True)
    tracking_links = Column(String, nullable=True)
    promo_codes = Column(String, nullable=True)

    status = Column(Enum(CampaignStatus), default=CampaignStatus.draft, nullable=False)
    created_at = Column(DateTime, server_default="NOW()")
    updated_at = Column(DateTime, onupdate="NOW()")
