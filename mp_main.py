import schedule
import os
import asyncio
from mp_modules.yamarket import yandex_market
from mp_modules.wb import wildberries
from utils.database import init_db
from proxy_list import proxy_config
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv()
goods_str = os.getenv("goods")
goods = goods_str.split(",") if goods_str else []

mp_frequency = int(os.getenv("mp_frequency"))
logger.info(f"{goods}")
logger.info(f"{mp_frequency}")


async def init():
    await init_db()


async def process_goods():
    """Процесс обработки товаров"""
    # Сначала выполняем yandex_market для каждого товара
    await asyncio.gather(*(yandex_market(good, proxy_config) for good in goods))

    # Затем выполняем wildberries для каждого товара
    await asyncio.gather(*(wildberries(good, proxy_config) for good in goods))


async def schedule_runner():
    """Асинхронный планировщик, запускающий задачи"""
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)  # Проверяем расписание каждую секунду


def schedule_jobs(loop):
    """Планирование задач с использованием существующего цикла событий"""
    # Планируем выполнение задачи каждые 30 секунд
    schedule.every(mp_frequency).seconds.do(lambda: loop.create_task(process_goods()))


async def main():
    # Инициализация базы данных
    await init()

    # Создаем расписание задач
    loop = asyncio.get_event_loop()
    schedule_jobs(loop)

    # Запуск планировщика
    await schedule_runner()


# Запуск программы
if __name__ == "__main__":
    asyncio.run(main())
