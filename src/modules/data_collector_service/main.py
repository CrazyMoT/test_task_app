from fastapi import FastAPI
from prometheus_client import generate_latest
from prometheus_client.exposition import CONTENT_TYPE_LATEST
from fastapi.responses import PlainTextResponse

from routes import sales
import uvicorn

app = FastAPI()

app.include_router(sales.router, prefix="/sales", tags=["sales"])

# Эндпоинт для метрик Prometheus
@app.get("/metrics", response_class=PlainTextResponse)
async def metrics():
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)