from modules.data_processor_service.logger import logger

from modules.common.models.models import Transaction
from modules.common.schemas.schemas import Sale
from modules.common.services.database import get_session

from sqlalchemy.future import select


async def process_data(data: dict) -> Sale:
    transaction_id = data.get('transaction_id')

    async with get_session() as session:
        # Проверка наличия транзакции с данным идентификатором
        transaction_query = select(Transaction).where(Transaction.transaction_id == transaction_id)
        result = await session.execute(transaction_query)
        transaction = result.scalar_one_or_none()

    if transaction is None:
        return Sale(**data)
    else:
        logger.warning(f'Transaction with id {transaction_id} already exists')
