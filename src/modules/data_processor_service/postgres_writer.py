from src.modules.shared.models.models import Transaction
from src.modules.shared.database import get_session
from src.modules.data_processor_service.logger import logger

from src.modules.shared.schemas.schemas import Sale


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
