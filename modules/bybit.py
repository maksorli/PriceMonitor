
import aiohttp
import asyncio
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Bybit:
    """Класс для взаимодействия с биржей Bybit """

    def __init__(self, pairs=None, category="spot"):
        self.pairs = (
            pairs
            if pairs
            else ["BTCUSDT", "ETHBTC", "XMRBTC", "SOLBTC", "BTCRUB", "DOGEBTC"]
        )
        self.api_url = "https://api.bybit.com/v5/market/tickers"
        self.category = category  # Добавляем категорию для запроса

    async def fetch_price(self, session, pair):
        params = {"symbol": pair, "category": self.category}  # Добавляем параметр категории
        try:
            async with session.get(self.api_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and "retCode" in data and data["retCode"] == 0:
                        # Логируем последнюю цену для пары
                        price = data["result"]["list"][0]["lastPrice"]
                        logger.info(f"{pair} - {price}")
                        return price
                    else:
                        logger.error(f"Ошибка в данных для {pair}: {data}")
                        return None
                elif response.status == 429:
                    logger.error(f"Ошибка 429: слишком много запросов для {pair}. Ждем 1 минуту...")
                    await asyncio.sleep(60)  # Асинхронная задержка на 60 секунд
                    return await self.fetch_price(session, pair)  # Повторяем запрос
                else:
                    logger.error(f"Ошибка: Статус {response.status} для {pair}")
                    return None
        except Exception as e:
            logger.error(f"Произошла ошибка при запросе для {pair}: {e}")
            return None

    async def get_prices(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_price(session, pair) for pair in self.pairs]
            return await asyncio.gather(*tasks)  # Выполняем все запросы асинхронно

 

    async def get_prices(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_price(session, pair) for pair in self.pairs]
            return await asyncio.gather(*tasks)  # Выполняем все запросы асинхронно