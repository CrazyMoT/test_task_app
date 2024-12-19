from modules.analytics_service.logger import logger
from modules.analytics_service.schemas.schemas import SaleReport
import datetime

from modules.analytics_service.services.reports_gen_database import ReportGenerator


def get_day_boundaries():
    now = datetime.datetime.now()
    start_of_day = datetime.datetime(now.year, now.month, now.day, 0, 0, 0)
    end_of_day = start_of_day + datetime.timedelta(days=1)
    return start_of_day, end_of_day


async def generate_daily_sales_report():
    start_of_day, end_of_day = get_day_boundaries()
    report_generator = ReportGenerator()
    transactions = await report_generator.get_transactions_in_day(start_of_day, end_of_day)
    for transaction in transactions:
        sale = SaleReport(
            product_id=transaction.product_id,
            total_sales=transaction.total_sales,
            average_purchase_value=transaction.average_purchase_value,
            timestamp=transaction.timestamp
        )
        await report_generator.write_report(sale)
    logger.info('Done generating daily sales report')
