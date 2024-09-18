import aiohttp
import logging
import asyncio

logger = logging.getLogger(__name__)


class CryptoExchange:
    """Базовый класс"""

    api_url = None  # URL API биржи, должен быть определен в дочерних классах
    pairs = []  # Список валютных пар

    def __init__(self, pairs=None, amount=3):
        if pairs:
            self.pairs = pairs
        self.amount = amount  # Количество денег на кошельке

    async def fetch_price(self, session, pair):
        """Получаем цену, нужно переопределить в дочерних классах"""
        raise NotImplementedError("Метод fetch_price должен быть переопределен")

    async def get_prices(self):
        """Получения цен по всем валютным парам, перепоределить в Coinmarket, bybit"""
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_price(session, pair) for pair in self.pairs]
            return await asyncio.gather(*tasks)
