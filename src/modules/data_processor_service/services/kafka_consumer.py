from confluent_kafka import Consumer, KafkaException, KafkaError
from prometheus_client import Counter, Histogram
import json
import time
from modules.data_processor_service.config import Config
from modules.data_processor_service.logger import logger

from .data_processing import process_data
from .postgres_writer import write_to_postgres

# Количество сообщений, обработанных консьюмером
messages_processed = Counter('kafka_messages_processed', 'Number of messages processed', ['topic', 'partition'])

# Количество ошибок, произошедших при потреблении сообщений
errors_occurred = Counter('kafka_consumer_errors', 'Number of errors occurred while consuming messages', ['topic', 'partition'])

# Время, затраченное на обработку сообщения
processing_time = Histogram('kafka_message_processing_duration_seconds', 'Time spent processing a message', ['topic', 'partition'])


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
            start_time = time.time()  # Засекаем время обработки сообщения
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    logger.info(f"{msg.topic()} [{msg.partition()}] reached end at offset {msg.offset()}")
                else:
                    errors_occurred.labels(topic=msg.topic(), partition=str(msg.partition())).inc()
                    raise KafkaException(msg.error())
            else:
                logger.info(f"Consumed message: {msg.value().decode('utf-8')}")
                data = json.loads(msg.value().decode('utf-8'))
                processed_data = await process_data(data)
                if processed_data:
                    await write_to_postgres(processed_data)
                # Увеличиваем счетчик сообщений после успешной обработки
                messages_processed.labels(topic=msg.topic(), partition=str(msg.partition())).inc()

                # Замеряем время обработки и обновляем гистограмму
                processing_time.labels(topic=msg.topic(), partition=str(msg.partition())).observe(
                    time.time() - start_time)

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
