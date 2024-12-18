FROM python:3.11-slim

WORKDIR /analytics_service


COPY ../../../requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Убедитесь, что контекст сборки правильный, и путь копирования соответствует
COPY ./src/modules/analytics_service /analytics_service

# Копирование общих файлов
COPY ./src/modules/shared /shared

# Настройка PYTHONPATH для доступа к общим модулям
ENV PYTHONPATH="${PYTHONPATH}:/shared:/analytics_service"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5002"]
#CMD ["sleep", "6600"]