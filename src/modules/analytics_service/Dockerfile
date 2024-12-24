FROM python:3.11-slim

WORKDIR /src


COPY ../../../requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Убедитесь, что контекст сборки правильный, и путь копирования соответствует
COPY ./src/modules/analytics_service /src/modules/analytics_service

# Копирование общих файлов
COPY ./src/modules/common /src/modules/common

# Установка PYTHONPATH для доступа к модулям из src
ENV PYTHONPATH="${PYTHONPATH}:/src"

CMD python /src/modules/analytics_service/main.py & python /src/modules/analytics_service/services/analys_service.py

#CMD ["python", "/src/modules/analytics_service/main.py"]
#CMD ["python", "/src/modules/analytics_service/services/analys_service.py"]
##CMD ["sleep", "6600"]