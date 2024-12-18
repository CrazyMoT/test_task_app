from loguru import logger
import sys

# Настройка loguru для логирования в консоль и файл
logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")
logger.add("logs/data_processor.log", format="{time} {level} {message}", level="DEBUG", rotation="1 MB")

# Экспорт логгера для использования в других модулях
__all__ = ["logger"]
