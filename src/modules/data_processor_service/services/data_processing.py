from ..models.models import Trash
from datetime import datetime

from modules.common.schemas.schemas import Sale
from modules.common.services.database import get_session


async def process_data(data: dict) -> Sale:
    async with get_session() as session:
        trash = await session.get(Trash, ident=1)

    # Проверка на пограничные кейсы
    if data['amount'] < trash.trashold:
        raise ValueError("Amount cannot be negative")

    # Вычисление метрик (если необходимо)
    data['timestamp'] = datetime.fromisoformat(data['timestamp'])

    return Sale(**data)
