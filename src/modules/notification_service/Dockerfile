FROM python:3.11-slim

WORKDIR /src

COPY ../../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Убедитесь, что контекст сборки правильный, и путь копирования соответствует
COPY ./src/modules/notification_service /src/modules/notification_service

# Копирование общих файлов
COPY ./src/modules/common /src/modules/common

# Установка PYTHONPATH для доступа к модулям из src
ENV PYTHONPATH="${PYTHONPATH}:/src"


CMD ["python", "/src/modules/notification_service/main.py"]
