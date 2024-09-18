import aiohttp
import asyncio
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Bybit:
    """Класс для взаимодействия с биржей Bybit"""

    def __init__(self, pairs=None, category="spot"):
        self.pairs = pairs or [
            "BTCUSDT",
            "ETHBTC",
            "XMRBTC",
            "SOLBTC",
            "BTCRUB",
            "DOGEBTC",
        ]
        self.api_url = "https://api.bybit.com/v5/market/tickers"
        self.category = category

    async def fetch_price(self, session, pair):
        params = {
            "symbol": pair,
            "category": self.category,
        }
        try:
            async with session.get(self.api_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and data.get("retCode") == 0:
                        price = data["result"]["list"][0]["lastPrice"]
                        logger.info(f"{pair} - {price}")
                        # Используем Decimal для точных вычислений, делае оратное преобразование
                        if pair in ["ETHBTC", "XMRBTC", "SOLBTC", "DOGEBTC"]:
                            return Decimal("1") / Decimal(price)
                        return Decimal(price)
                    else:
                        logger.error(f"Ошибка в данных для {pair}: {data}")
                else:
                    logger.error(f"Ошибка: Статус {response.status} для {pair}")
        except Exception as e:
            logger.error(f"Произошла ошибка при запросе для {pair}: {e}")
        return None

    async def get_prices(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_price(session, pair) for pair in self.pairs]
            return await asyncio.gather(*tasks)
