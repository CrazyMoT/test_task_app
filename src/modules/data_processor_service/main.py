import asyncio
from prometheus_client import start_http_server
from modules.data_processor_service.services.kafka_consumer import consume

async def start_prometheus_server():
    start_http_server(5004)

async def main():
    # Запускаем сервер Prometheus в фоновом режиме
    await asyncio.gather(
        start_prometheus_server(),
        consume()  # Асинхронно запускаем Kafka Consumer
    )

if __name__ == "__main__":
    asyncio.run(main())
