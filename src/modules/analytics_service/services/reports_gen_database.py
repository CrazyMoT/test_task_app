from modules.common.models.models import Transaction
from modules.common.services.database import get_session

from modules.analytics_service.models.models import Analytics
from modules.analytics_service.logger import logger
from modules.analytics_service.schemas.schemas import SaleReport

from sqlalchemy.future import select
from sqlalchemy import func

class ReportGenerator:

    async def get_transactions_in_day(self, start_of_day, end_of_day):
        async with get_session() as session:
            result = await session.execute(
                select(
                    Transaction.product_id,
                    func.sum(Transaction.total_amount).label('total_sales'),
                    func.avg(Transaction.total_amount).label('average_purchase_value')
                ).where(
                    Transaction.timestamp >= start_of_day,
                    Transaction.timestamp < end_of_day
                ).group_by(
                    Transaction.product_id
                )
            )

            return result.all()

    async def write_report(self, data: SaleReport):
        async with get_session() as session:
            analytics_entry = Analytics(
                product_id=data.product_id,
                total_sales=data.total_sales,
                average_purchase_value=data.average_purchase_value,
                timestamp=data.timestamp
            )
            session.add(analytics_entry)
            await session.commit()
            logger.info("Data written to PostgreSQL")



