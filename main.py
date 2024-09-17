import asyncio
from database import init_db
import logging
import time
import schedule
from utils import fetch_prices

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Функция для инициализации базы данных
async def init():
    await init_db()

# Функция-обертка для запуска асинхронных задач через schedule
def run_async_task(task):
    asyncio.run(task())

# Основной запуск с использованием schedule
def main():
    # Инициализация базы данных
    asyncio.run(init())

    # Добавляем задачу в расписание  
    schedule.every(5).seconds.do(run_async_task, fetch_prices)

    while True:
        # Проверяем расписание и выполняем задачи
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()