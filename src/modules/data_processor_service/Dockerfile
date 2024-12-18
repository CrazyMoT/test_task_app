FROM python:3.11-slim

WORKDIR /data_processor_service

COPY ../../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Убедитесь, что контекст сборки правильный, и путь копирования соответствует
COPY ./src/modules/data_processor_service /data_processor_service

# Копирование общих файлов
COPY ./src/modules/shared /shared

# Настройка PYTHONPATH для доступа к общим модулям
ENV PYTHONPATH="${PYTHONPATH}:/shared:/data_processor_service"


CMD ["python", "main.py"]
#CMD ["sleep", "6600"]