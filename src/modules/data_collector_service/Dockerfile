FROM python:3.11-slim

WORKDIR /src

# Установка зависимостей
COPY ../../../requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копирование только содержимого папки data_collector_service
COPY ./src/modules/data_collector_service /src/modules/data_collector_service

# Копирование общих файлов
COPY ./src/modules/common /src/modules/common

# Установка PYTHONPATH для доступа к модулям из src
ENV PYTHONPATH="${PYTHONPATH}:/src"

# Запуск приложения
CMD ["python", "/src/modules/data_collector_service/main.py"]