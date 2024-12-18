from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    kafka_bootstrap_servers: str
    kafka_topic: str
    threshold: int

    class Config:
        env_file = ".env"

settings = Settings()
