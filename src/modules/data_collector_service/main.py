from fastapi import FastAPI
from routes import sales

app = FastAPI()

app.include_router(sales.router, prefix="/sales", tags=["sales"])
