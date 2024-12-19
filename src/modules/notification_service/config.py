from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    kafka_broker: str
    kafka_topic: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), '.env')  # Путь к .env файлу

settings = Settings()
