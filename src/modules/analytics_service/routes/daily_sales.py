from fastapi import APIRouter, Query
from typing import Union, List

from models.report_fetcher_database import ReportFetcher
from schemas import SaleReportWithProductName

router = APIRouter()

@router.get("/daily_sales", response_model=Union[SaleReportWithProductName, List[SaleReportWithProductName]])
async def get_daily_sales(product_id: int = Query(None)):
    report_fetcher = ReportFetcher()
    if product_id:
        report = await report_fetcher.get_latest_report(product_id)
        return report
    else:
        reports = await report_fetcher.get_latest_reports()
        return reports
