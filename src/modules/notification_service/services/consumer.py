import asyncio
from confluent_kafka import Consumer, KafkaError
from modules.notification_service.config import settings
from .notifier import handle_notification


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
                print(msg.error())
                continue

        data = msg.value().decode('utf-8')
        await handle_notification(data)


async def start_consume():
    consumer = create_consumer()
    try:
        await consume_notifications(consumer)
    finally:
        consumer.close()



