import os
import aiohttp
from dotenv import load_dotenv
from modules.cryptoexchange import CryptoExchange  # Базовый класс Exchange
import asyncio
import logging
from decimal import Decimal
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
# Загружаем переменные окружения из .env
load_dotenv()

COINMARKET_API_KEY = os.getenv("COINMARKETCAP_API_KEY")

if not COINMARKET_API_KEY:
    raise ValueError(
        "API ключ для CoinMarketCap не найден"
    )


class CoinMarketCap(CryptoExchange):
    """Класс для взаимодействия с API CoinMarketCap"""

    api_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    async def fetch_price(self, session, pair):
        symbol, convert = pair
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": COINMARKET_API_KEY,
        }
        params = {"symbol": symbol, "convert": convert}

        async with session.get(
            self.api_url, headers=headers, params=params
        ) as response:
            data = await response.json()
            if "data" in data and symbol in data["data"]:
                price = data["data"][symbol]["quote"][convert]["price"]
                logger.info(f"{symbol}/{convert} - {price}")
                return Decimal(price)
            else:
                logger.info(
                    f"Ошибка: Нет данных для {symbol}/{convert} на CoinMarketCap"
                )
                return None

    async def get_prices(self):
        pairs = [
            ("BTC", "USDT"),
            ("BTC", "ETH"),
            ("BTC", "XMR"),
            ("BTC", "SOL"),
            ("BTC", "RUB"),
            ("BTC", "DOGE"),
        ]
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_price(session, pair) for pair in pairs]
            prices = await asyncio.gather(
                *tasks
            )  # Собираем результаты выполнения задач
            return prices  # Возвращаем список цен
