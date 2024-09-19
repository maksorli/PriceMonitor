from modules.cryptoexchange import CryptoExchange
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Binance(CryptoExchange):
    """Класс для взаимодействия с биржей Binance"""

    api_url = "https://api.binance.com/api/v3/ticker/price"

    async def fetch_price(self, session, pair):
        params = {"symbol": pair}
        async with session.get(self.api_url, params=params) as response:
            data = await response.json()

            # проверяем и проводим  обратное преобразование для пар /BTC
            if "price" in data:
                logger.info(f"{pair} - {data['price']}")
                if pair in ["ETHBTC", "XMRBTC", "SOLBTC", "DOGEBTC"]:
                    return 1 / Decimal(data["price"])
                return Decimal(data["price"])

            else:
                # logger.error(f"Ошибка: Нет цены для {pair} на Binance")
                return None
