from sqlalchemy import Column, Integer

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Trash(Base):
    __tablename__ = 'trash'
    t_id = Column(Integer, primary_key=True, autoincrement=True)
    trashold = Column(Integer, default=1, nullable=False)