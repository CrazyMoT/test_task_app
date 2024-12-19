import asyncio
from modules.data_processor_service.services.kafka_consumer import consume

if __name__ == "__main__":
    asyncio.run(consume())