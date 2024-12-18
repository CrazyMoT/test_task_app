FROM python:3.11-slim

WORKDIR /data_collector_service

# Установка зависимостей
COPY ../../../requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копирование только содержимого папки data_collector_service
COPY ./src/modules/data_collector_service/ .

# Копирование общих файлов
COPY ./src/modules/shared /shared

# Настройка PYTHONPATH для доступа к общим модулям
ENV PYTHONPATH="${PYTHONPATH}:/shared:/data_collector_service"

# Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]
#CMD ["sleep", "6600"]