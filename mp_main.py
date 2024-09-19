from mp_modules.yamarket import yandex_market
from mp_modules.wb import wildberries
import asyncio
from utils.database import init_db
from proxy_list import proxy_config


goods = ["копье", "дуршлаг", "красные носки", "леска для спиннинга"]


async def init():
    await init_db()


async def main():
    # Инициализация базы данных
    await init()

    # Сначала выполняем yandex_market для каждого товара
    await asyncio.gather(*(yandex_market(good, proxy_config) for good in goods))

    # Затем выполняем wildberries для каждого товара
    await asyncio.gather(*(wildberries(good, proxy_config) for good in goods))


# Запуск программы
if __name__ == "__main__":
    asyncio.run(main())
