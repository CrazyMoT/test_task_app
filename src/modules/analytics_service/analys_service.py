from src.modules.notification_service.config import settings
from schemas import SaleReportWithProductName
from typing import List
from report_generator import generate_daily_sales_report
from .models.setteings_analysis import get_latest_analytics_settings
from src.modules.analytics_service.models.report_fetcher_database import ReportFetcher
from src.modules.shared.kafka_producer import KafkaProducerService

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio

async def daily_analysis():
    await generate_daily_sales_report()
    kafka_producer = KafkaProducerService(settings=settings)
    reports: List[SaleReportWithProductName] = await ReportFetcher().get_latest_reports()
    latest_settings = await get_latest_analytics_settings()
    minimum_sales = latest_settings.minimum_sales
    for report in reports:
        if not report.total_sales < minimum_sales:
            kafka_producer.send(report.product_name, value=report)


def run_daily_analysis():
    asyncio.run(daily_analysis())


def task_daily_analysis():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_daily_analysis, 'cron', hour=0)  # Запуск каждый день в полночь
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    task_daily_analysis()
