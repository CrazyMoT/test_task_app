from datetime import datetime
from pydantic import BaseModel, ConfigDict

class Sale(BaseModel):
    transaction_id: int
    product_id: int
    quantity: int
    amount: float
    timestamp: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)

class SaleReportWithProductName(BaseModel):
    product_name: str
    total_sales: float
    average_purchase_value: float
    timestamp: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)