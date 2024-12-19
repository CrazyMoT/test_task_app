from services.consumer import start_consume
import asyncio


if __name__ == "__main__":
    asyncio.run(start_consume())