from confluent_kafka import Producer

class KafkaProducerService:
    def __init__(self,  settings):
        self.settings = settings
        self.producer = Producer({'bootstrap.servers': self.settings.kafka_broker})

    def delivery_report(self, err, msg):
        if err is not None:
            print(f"Message delivery failed: {err}")
        else:
            print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def send(self, key, value):
        self.producer.produce(self.settings.kafka_topic, key=key, value=value, callback=self.delivery_report)
        self.producer.poll(1)
