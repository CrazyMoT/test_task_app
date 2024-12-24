from modules.data_processor_service.logger import logger
from modules.common.models.models import Transaction
from modules.common.services.database import get_session
from modules.common.schemas.schemas import Sale


async def write_to_postgres(data: Sale):
    # Убираем временную зону с помощью replace(tzinfo=None)
    timestamp_naive = data.timestamp.replace(tzinfo=None)

    async with get_session() as session:
        transaction = Transaction(
            transaction_id=data.transaction_id,
            product_id=data.product_id,
            quantity=data.quantity,
            total_amount=data.amount,
            timestamp=timestamp_naive,
        )
        session.add(transaction)
        await session.commit()
        logger.info("Data written to PostgreSQL")
