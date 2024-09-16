from modules.cryptoexchange import CryptoExchange
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class KuCoin(CryptoExchange):
    """Класс для взаимодействия с биржей KuCoin"""

    api_url = "https://api.kucoin.com/api/v1/market/allTickers"

    async def fetch_price(self, session, pair):
        async with session.get(self.api_url) as response:
            data = await response.json()
            tickers = data["data"]["ticker"]
            for ticker in tickers:
                if ticker["symbol"] == pair:
                    logger.info(f"{pair} - {ticker['last']}")
                    return float(ticker["last"])
            logger.error(f"Ошибка: Нет данных для {pair} на KuCoin")
            return None
