import datetime
from typing import List
from pydantic import BaseModel, ConfigDict

class SaleReport(BaseModel):
    product_id: int
    total_sales: int
    average_purchase_value: float
    timestamp: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)

class SaleReportList(BaseModel):
    reports: List[SaleReport]

class SaleReportWithProductName(BaseModel):
    product_name: str
    total_sales: float
    average_purchase_value: float
    timestamp: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)