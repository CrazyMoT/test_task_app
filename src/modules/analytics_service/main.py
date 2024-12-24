from fastapi import FastAPI
from prometheus_client import generate_latest
from prometheus_client.exposition import CONTENT_TYPE_LATEST
from fastapi.responses import PlainTextResponse

import uvicorn

from modules.analytics_service.routes import daily_sales

app = FastAPI()

app.include_router(daily_sales.router, prefix="/sales", tags=["sales"])



@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    # Запускаем сервер FastAPI
    uvicorn.run(app, host="0.0.0.0", port=5002)
