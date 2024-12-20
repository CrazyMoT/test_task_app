from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from modules.common.models.models import Base


class Analytics(Base):
    __tablename__ = 'analytics'
    id = Column(Integer, primary_key=True, autoincrement=True)

    product_id = Column(Integer, ForeignKey('products.product_id'))
    total_sales = Column(Float)
    average_purchase_value = Column(Float)
    timestamp = Column(DateTime)

    product = relationship("Product")


class AnalyticsSettings(Base):
    __tablename__ = 'analytics_settings'
    id = Column(Integer, primary_key=True, autoincrement=True)

    minimum_sales = Column(Integer, default=10, nullable=False)