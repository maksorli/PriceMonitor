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
from utils import pair_dict

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def main():
    # Инициализация базы данных
    await init_db()


async def main():

    pairs = [
        "BTC/USDT",
        "ETH/BTC",
        "XMR/BTC",
        "SOL/BTC",
        "BTC/RUB",
        "DOGE/BTC",
    ]  # порядок пар

    # Инициализация объектов для каждой биржи
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
        bybit.get_prices(),
    )

    # Логируем результаты от каждой биржи
    logger.info(f"Binance: {all_prices[0]}")
    logger.info(f"CoinMar: {all_prices[1]}")
    logger.info(f" GateIO: {all_prices[2]}")
    logger.info(f" KuCoin: {all_prices[3]}")
    logger.info(f"  Bybit: {all_prices[4]}")

    all_pairs_prices = pair_dict(all_prices)

    # Логируем общий список котировок по всем парам
    logger.info(f"Все пары с ценами: {all_pairs_prices}")

    # Далее можно выбирать лучшие цены и сохранять в базу данных...


if __name__ == "__main__":
    asyncio.run(main())
