from prometheus_client import start_http_server
from services.consumer import start_consume
import asyncio


async def start_prometheus_server():
    start_http_server(5003)

async def main():
    # Запускаем сервер Prometheus в фоновом режиме
    await asyncio.gather(
        start_prometheus_server(),
        start_consume()  # Асинхронно запускаем Kafka Consumer
    )

if __name__ == "__main__":
    asyncio.run(main())