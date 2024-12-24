from modules.analytics_service.logger import logger

from modules.analytics_service.config import settings
from modules.common.schemas.schemas import SaleReportWithProductName
from typing import List

from report_generator import generate_daily_sales_report

from setteings_analysis import get_latest_analytics_settings
from report_fetcher_database import ReportFetcher
from modules.common.services.kafka_producer import KafkaProducerService

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import json
from datetime import datetime


def custom_json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.timestamp()
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')


async def daily_analysis():
    logger.info(f'Analysis task start')
    await generate_daily_sales_report()
    kafka_producer = KafkaProducerService(settings=settings)
    reports: List[SaleReportWithProductName] = await ReportFetcher().get_latest_reports()
    latest_settings = await get_latest_analytics_settings()
    minimum_sales = latest_settings.minimum_sales
    for report in reports:
        if not report.total_sales < minimum_sales:
            if not report.total_sales < minimum_sales:
                report_json = json.dumps(report.__dict__, default=custom_json_serializer)  # Сериализуем объект в JSON строку
                report_bytes = report_json.encode('utf-8')  # Преобразуем JSON строку в байты
                kafka_producer.send(report.product_name, value=report_bytes)


async def run_daily_analysis():
    await daily_analysis()


async def task_daily_analysis():
    scheduler = AsyncIOScheduler()
    logger.info(f'Analysis task start')
    scheduler.add_job(run_daily_analysis, 'interval', minutes=1)
    # scheduler.add_job(run_daily_analysis, 'cron', hour=0)  # Запуск каждый день в полночь
    scheduler.start()

    await asyncio.Event().wait()


if __name__ == '__main__':
    asyncio.run(task_daily_analysis())
