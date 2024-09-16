import asyncio
from modules.binance import Binance
from modules.coinmarketcap import CoinMarketCap
from modules.bybit import Bybit
from modules.gateio import GateIO
from modules.kucoin import KuCoin
from csv_writer import write_to_csv
from database import init_db, save_price
from mail_sender import send_email
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def main():
    # Инициализация базы данных
    await init_db()


async def main():
    # Инициализация объектов для каждой биржи
    pairs = ["BTC/USDT", "ETH/BTC", "XMR/BTC", "SOL/BTC", "BTC/RUB", "DOGE/BTC"]
    binance = Binance(["BTCUSDT", "ETHBTC", "XMRBTC", "SOLBTC", "BTCRUB", "DOGEBTC"])
    gateio = GateIO(
        ["BTC_USDT", "ETH_BTC", "XMR_BTC", "SOL_BTC", "RUB_BTC", "DOGE_BTC"]
    )
    kucoin = KuCoin(
        ["BTC-USDT", "ETH-BTC", "XMR-BTC", "SOL-BTC", "RUB-BTC", "DOGE-BTC"]
    )
    coinmarketcap = CoinMarketCap()
    
    bybit = Bybit()

    # Получаем котировки с бирж
    all_prices = await asyncio.gather(
        binance.get_prices(),
        coinmarketcap.get_prices(),
        gateio.get_prices(),
        kucoin.get_prices(),
        bybit.get_prices()
    )
    all_prices[0][1]=1/all_prices[0][1]
    all_prices[0][2]=1/all_prices[0][2]
    all_prices[0][3]=1/all_prices[0][3]
    all_prices[2][1]=1/all_prices[2][1]
    all_prices[2][2]=1/all_prices[2][2]
    all_prices[2][5]=1/all_prices[2][5]
    all_prices[3][1]=1/all_prices[3][1]
    all_prices[3][2]=1/all_prices[3][2]
    all_prices[3][5]=1/all_prices[3][5]
    

    # Логируем результаты от каждой биржи
    logger.info(f"Binance: {all_prices[0]}")
    logger.info(f"CoinMar: {all_prices[1]}")
    logger.info(f" GateIO: {all_prices[2]}")
    logger.info(f" KuCoin: {all_prices[3]}")
    logger.info(f"Ц Bybit: {all_prices[4]}")
    # Обрабатываем котировки для каждой валютной пары
    all_pairs_prices = []

    for i, pair in enumerate(pairs):
        prices_for_pair = []
        for prices in all_prices:
            if prices is not None and i < len(prices):
                prices_for_pair.append(prices[i])  # Добавляем цену для пары
            else:
                prices_for_pair.append(None)  # Если данных нет, добавляем None
        all_pairs_prices.append(prices_for_pair)

    # Логируем общий список котировок по всем парам
    logger.info(f"Все пары с ценами: {all_pairs_prices}")

    # Далее можно выбирать лучшие цены и сохранять в базу данных...


if __name__ == "__main__":
    asyncio.run(main())
