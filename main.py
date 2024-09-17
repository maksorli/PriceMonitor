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
    loop = asyncio.get_event_loop()  # Получаем текущий event loop
    loop.create_task(task())  # Создаем задачу в текущем event loop


# Основной запуск с использованием schedule
async def main():
    # Инициализация базы данных
    await init()

    # Добавляем задачу в расписание  
    schedule.every(5).seconds.do(run_async_task, fetch_prices)

    while True:
        # Проверяем расписание и выполняем задачи
        schedule.run_pending()
        await asyncio.sleep(1)  # Используем асинхронный sleep

if __name__ == "__main__":
    try:
        asyncio.run(main())  # Запускаем главный цикл событий
    except KeyboardInterrupt:
        logger.info("Программа остановлена пользователем")