from fastapi import APIRouter, Query, Request
from prometheus_client import Counter, Histogram
from typing import Union, List


from modules.analytics_service.services.report_fetcher_database import ReportFetcher
from modules.common.schemas.schemas import SaleReportWithProductName


REQUEST_COUNT = Counter('request_count', 'Total number of requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency', ['endpoint'])


router = APIRouter()

@router.get("/daily_sales", response_model=Union[SaleReportWithProductName, List[SaleReportWithProductName]])
async def get_daily_sales(request: Request, product_id: int = Query(None)):
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    with REQUEST_LATENCY.labels(endpoint=request.url.path).time():
        report_fetcher = ReportFetcher()
        if product_id:
            report = await report_fetcher.get_latest_report(product_id)
            return report
        else:
            reports = await report_fetcher.get_latest_reports()
            return reports
