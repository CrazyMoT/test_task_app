
from config import settings

async def handle_notification(data):
    sales = int(data)
    if sales < settings.threshold:
        await send_alert(f"Sales have dropped below threshold: {sales}")

async def send_alert(message: str):
    # Логика отправки уведомления (например, через email, SMS или другие сервисы)
    print(message)
