from modules.cryptoexchange import CryptoExchange
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Binance(CryptoExchange):
    """Класс для взаимодействия с биржей Binance"""

    api_url = "https://api.binance.com/api/v3/ticker/price"

    async def fetch_price(self, session, pair):
        params = {"symbol": pair}
        async with session.get(self.api_url, params=params) as response:
            data = await response.json()
            if "price" in data:
                logger.info(f"{pair} - {data['price']}")
                return float(data["price"])
            else:
                logger.error(f"Ошибка: Нет цены для {pair} на Binance")
                return None
