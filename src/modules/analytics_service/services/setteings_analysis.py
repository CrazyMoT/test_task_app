from modules.analytics_service.models.models import AnalyticsSettings
from modules.common.services.database import get_session
from sqlalchemy.future import select


async def get_latest_analytics_settings() -> AnalyticsSettings:
    async with get_session() as session:
        result = await session.execute(
            select(AnalyticsSettings).order_by(AnalyticsSettings.id.desc())
        )
        latest_settings = result.scalars().first()
        return latest_settings