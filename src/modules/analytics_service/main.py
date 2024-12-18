from fastapi import FastAPI
from routes import daily_sales


app = FastAPI()

app.include_router(daily_sales.router, prefix="/sales", tags=["sales"])

