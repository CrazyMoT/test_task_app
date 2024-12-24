import asyncio
import time
from confluent_kafka import Consumer, KafkaError, KafkaException
from prometheus_client import Counter, Histogram
from modules.notification_service.config import settings
from .notifier import handle_notification


# Количество сообщений, обработанных консьюмером
messages_processed = Counter('kafka_messages_processed', 'Number of messages processed', ['topic', 'partition'])
# Количество ошибок, произошедших при потреблении сообщений
errors_occurred = Counter('kafka_consumer_errors', 'Number of errors occurred while consuming messages', ['topic', 'partition'])
# Время, затраченное на обработку сообщения
processing_time = Histogram('kafka_message_processing_duration_seconds', 'Time spent processing a message', ['topic', 'partition'])


def create_consumer():
    consumer = Consumer({
        'bootstrap.servers': settings.kafka_broker,
        'group.id': 'notification_service_group',
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([settings.kafka_topic])
    return consumer


async def consume_notifications(consumer):
    while True:
        start_time = time.time()  # Засекаем время обработки сообщения
        msg = consumer.poll(1.0)  # ожидание сообщения в течение 1 секунды
        if msg is None:
            await asyncio.sleep(1)
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # Конец раздела
                continue
            else:
                # Ошибка сообщения
                errors_occurred.labels(topic=msg.topic(), partition=str(msg.partition())).inc()
                raise KafkaException(msg.error())

        data = msg.value().decode('utf-8')
        await handle_notification(data)
        # Увеличиваем счетчик сообщений после успешной обработки
        messages_processed.labels(topic=msg.topic(), partition=str(msg.partition())).inc()

        # Замеряем время обработки и обновляем гистограмму
        processing_time.labels(topic=msg.topic(), partition=str(msg.partition())).observe(
            time.time() - start_time)


async def start_consume():
    consumer = create_consumer()
    try:
        await consume_notifications(consumer)
    finally:
        consumer.close()



