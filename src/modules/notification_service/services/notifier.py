from modules.notification_service.models.models import Trash
from modules.notification_service.logger import logger
from modules.common.services.database import get_session
from modules.common.schemas.schemas import SaleReportWithProductName
import json

async def handle_notification(data: str):
    data_dict = json.loads(data)
    validated_data = SaleReportWithProductName(**data_dict)
    sales = float(validated_data.total_sales)
    async with get_session() as session:
        trash = await session.get(Trash, ident=1)

    if sales < trash.trashold:
        await send_alert(f"Sales have dropped below threshold: {sales}")

async def send_alert(message: str):
    # Логика отправки уведомления (например, через email, SMS или другие сервисы)
    logger.warning(message)
