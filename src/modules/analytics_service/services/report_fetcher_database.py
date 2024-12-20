from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import List

from modules.analytics_service.models.models import Analytics
from modules.analytics_service.schemas.schemas import SaleReportWithProductName

from modules.common.models.models import Product
from modules.common.services.database import get_session


class ReportFetcher:
    async def get_latest_report(self, product_id: int = None) -> SaleReportWithProductName | None:
        async with get_session() as session:
            query = select(Analytics).options(joinedload(Product.name))
            if product_id:
                query = query.where(Analytics.product_id == product_id)
            query = query.order_by(Analytics.timestamp.desc())
            result = await session.execute(query)
            report = result.scalars().first()
            if report:
                return SaleReportWithProductName(
                    product_name=report.product.name,
                    total_sales=report.total_sales,
                    average_purchase_value=report.average_purchase_value,
                    timestamp=report.timestamp
                )
            return None

    async def get_latest_reports(self) -> List[SaleReportWithProductName]:
        async with get_session() as session:
            query = select(Analytics).options(joinedload(Analytics.product)).order_by(Analytics.timestamp.desc())
            result = await session.execute(query)
            reports = result.scalars().all()

            if not reports:
                return []

            latest_reports = {}
            for report in reports:
                if report.product_id not in latest_reports:
                    latest_reports[report.product_id] = report
            return [
                SaleReportWithProductName(
                    product_name=report.product.name,
                    total_sales=report.total_sales,
                    average_purchase_value=report.average_purchase_value,
                    timestamp=report.timestamp
                ) for report in latest_reports.values()
            ]
