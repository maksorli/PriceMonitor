from modules.cryptoexchange import CryptoExchange
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class GateIO(CryptoExchange):
    """Класс для взаимодействия с биржей Gate.io"""

    api_url = "https://api.gateio.ws/api/v4/spot/tickers"

    async def fetch_price(self, session, pair):
        params = {"currency_pair": pair}
        async with session.get(self.api_url, params=params) as response:
            data = await response.json()
            if data and isinstance(data, list) and len(data):
                logger.info(f"{pair} - {data[0]['last']}")
                if pair in ["ETH_BTC", "XMR_BTC", "SOL_BTC", "RUB_BTC", "DOGE_BTC"]:
                    return 1 / float(data[0]["last"])
                return float(data[0]["last"])

            else:
                logger.info(f"Ошибка: Нет данных для {pair} на Gate.io")
                return None
