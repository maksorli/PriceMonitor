from modules.cryptoexchange import CryptoExchange
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from decimal import Decimal


class KuCoin(CryptoExchange):
    """Класс для взаимодействия с биржей KuCoin"""

    api_url = "https://api.kucoin.com/api/v1/market/allTickers"

    async def fetch_price(self, session, pair):
        async with session.get(self.api_url) as response:
            data = await response.json()
            tickers = data["data"]["ticker"]
            for ticker in tickers:
                # проверяем и проводим  обратное преобразование для пар /BTC
                if ticker["symbol"] == pair:
                    logger.info(f"{pair} - {ticker['last']}")
                    if pair in ["ETH-BTC", "XMR-BTC", "SOL-BTC", "RUB-BTC", "DOGE-BTC"]:
                        return 1 / Decimal(ticker["last"])
                    return Decimal(ticker["last"])

            #logger.error(f"Ошибка: Нет данных для {pair} на KuCoin")
            return None
