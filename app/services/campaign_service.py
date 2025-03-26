from app.models.campaign import Campaign, CampaignStatus
from app.schemas.campaign import CampaignCreate, CampaignResponse, InfluencerCriteria, TargetAudience, \
    ContentRequirements, PerformanceMetrics, Budget


def create_campaign_entity(campaign_data: CampaignCreate) -> Campaign:
    return Campaign(
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
def map_campaign_to_response(campaign) -> CampaignResponse:
    return CampaignResponse(
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