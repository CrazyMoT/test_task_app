from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
import uvicorn

from contextlib import asynccontextmanager
from modules.analytics_service.routes import daily_sales
from modules.analytics_service.services.analys_service import daily_analysis

app = FastAPI()

app.include_router(daily_sales.router, prefix="/sales", tags=["sales"])

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Запуск планировщика при старте приложения
    scheduler.add_job(daily_analysis, 'cron', hour=0)  # Запуск каждый день в полночь
    scheduler.start()
    yield
    # Остановка планировщика при завершении работы приложения
    scheduler.shutdown()

app.router.lifespan = lifespan

if __name__ == "__main__":
    # Запускаем сервер FastAPI
    uvicorn.run(app, host="0.0.0.0", port=5002)
