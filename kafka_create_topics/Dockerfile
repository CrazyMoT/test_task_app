FROM python:3.11-slim

# Установим рабочую директорию
WORKDIR /create_kafka_topics

# Установим необходимые библиотеки
RUN pip install confluent-kafka

# Скопируем наш скрипт в контейнер
COPY . .


# Запуск скрипта
ENTRYPOINT ["python", "create_kafka_topics.py"]
