from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AnalyticsSettings(Base):
    __tablename__ = 'analytics_settings'
    id = Column(Integer, primary_key=True, autoincrement=True)

    minimum_sales = Column(Integer, default=10, nullable=False)