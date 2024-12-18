from confluent_kafka import Consumer, KafkaException, KafkaError
import json
from config import Config
from data_processing import process_data
from postgres_writer import write_to_postgres
from logger import logger

async def consume():
    conf = {
        'bootstrap.servers': Config.KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'data_processor_group',
        'auto.offset.reset': 'earliest',
    }

    consumer = Consumer(conf)
    consumer.subscribe([Config.KAFKA_TOPIC])

    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.info(f"{msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}")
                else:
                    raise KafkaException(msg.error())
            else:
                logger.info(f"Consumed message: {msg.value().decode('utf-8')}")
                data = json.loads(msg.value().decode('utf-8'))
                processed_data = await process_data(data)
                await write_to_postgres(processed_data)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
