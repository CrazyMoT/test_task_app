from modules.data_processor_service.logger import logger

from modules.common.models.models import Transaction
from modules.common.services.database import get_session
from modules.common.schemas.schemas import Sale


async def write_to_postgres(data: Sale):
    async with get_session() as session:
        transaction = Transaction(
            transaction_id=data.transaction_id,
            product_id=data.product_id,
            quantity=data.quantity,
            total_amount=data.amount,
            timestamp=data.timestamp,
        )
        session.add(transaction)
        await session.commit()
        logger.info("Data written to PostgreSQL")
