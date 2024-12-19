from loguru import logger
import sys
import os

# Определение пути для логов
log_dir = "/var/log/data_collector_service"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "data_collector.log")

# Настройка loguru для логирования в консоль и файл
logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")
logger.add(log_path, format="{time} {level} {message}", level="DEBUG", rotation="1 MB")

# Экспорт логгера для использования в других модулях
__all__ = ["logger"]
