from modules.common.models.models import Product, Transaction
from modules.analytics_service.models.models import Analytics
from modules.data_processor_service.models.models import Trash
from datetime import datetime, timedelta
import random
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


engine = create_async_engine('postgresql+asyncpg://user:password@localhost:5433/database', echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def add_test_data():
    async with async_session() as session:
        # Создание тестовых данных для таблицы Product
        products = [
            Product(name=f'Product {i}', category=f'Category {random.choice(["A", "B", "C"])}',
                    price=round(random.uniform(10, 100), 2))
            for i in range(1, 11)
        ]

        # Добавление данных в таблицу Product
        session.add_all(products)
        await session.commit()

        # Получаем id всех продуктов, которые были вставлены
        product_ids = [product.product_id for product in products]

        # Создание тестовых данных для таблицы Transaction
        transactions = [
            Transaction(product_id=random.choice(product_ids),
                        quantity=random.randint(1, 10),
                        total_amount=round(random.uniform(10, 200), 2),
                        timestamp=datetime.now() - timedelta(days=random.randint(1, 30)))
            for _ in range(10)
        ]

        # Добавление данных в таблицу Transaction
        session.add_all(transactions)
        await session.commit()

        # Создание тестовых данных для таблицы Analytics
        analytics = [
            Analytics(product_id=random.choice(product_ids),
                      total_sales=round(random.uniform(1000, 5000), 2),
                      average_purchase_value=round(random.uniform(50, 200), 2),
                      timestamp=datetime.now() - timedelta(days=random.randint(1, 30)))
            for _ in range(10)
        ]

        # Добавление данных в таблицу Analytics
        session.add_all(analytics)
        await session.commit()

async def add_trash():
    async with async_session() as session:
        new_trash = Trash(trashold=10)

        # Добавляем запись в сессию
        session.add(new_trash)

        # Сохраняем изменения в базе данных
        await session.commit()

if __name__ == '__main__':
    asyncio.run(add_test_data())  # Если вы хотите запустить отдельно в асинхронной среде
    # asyncio.run(add_trash())