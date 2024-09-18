import asyncio
from modules.binance import Binance
from modules.coinmarketcap import CoinMarketCap
from modules.bybit import Bybit
from modules.gateio import GateIO
from modules.kucoin import KuCoin
from modules.cryptoexchange import CryptoExchange
from mail_sender import send_email
import logging
from datetime import datetime
from decimal import Decimal
from csv_writer import write_to_csv
from json_writer import write_to_json
from database import PriceRecord

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

last_prices = {
    "Binance": {},
    "CoinMarketCap": {},
    "GateIO": {},
    "KuCoin": {},
    "Bybit": {},
}

# def pair_dict(all_prices):
#     """
#     Собираем список по валютным парам
#     """
#     all_pairs_prices = []
#     pairs = [
#         "BTC/USDT",
#         "ETH/BTC",
#         "XMR/BTC",
#         "SOL/BTC",
#         "BTC/RUB",
#         "DOGE/BTC",
#     ]  # порядок пар
#     for i, pair in enumerate(pairs):
#         prices_for_pair = []
#         for prices in all_prices:
#             if prices is not None and i < len(prices):
#                 prices_for_pair.append(prices[i])  # Добавляем цену для пары
#             else:
#                 prices_for_pair.append(None)  # Если данных нет, добавляем None
#         all_pairs_prices.append(prices_for_pair)
#     return all_pairs_prices


async def fetch_prices():
    global last_prices
    # порядок пар
    pairs = [
        "BTC/USDT",
        "BTC/ETH",
        "BTC/XMR",
        "BTC/SOL",
        "BTC/RUB",
        "BTC/DOGE",
    ]

    PRICE_CHANGE_THRESHOLD = Decimal("0.03")

    # Инициализация объектов для каждой биржи
    crypto_wallet = CryptoExchange()
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
    # logger.info(f"Binance: {all_prices[0]}")
    # logger.info(f"CoinMar: {all_prices[1]}")
    # logger.info(f" GateIO: {all_prices[2]}")
    # logger.info(f" KuCoin: {all_prices[3]}")
    # logger.info(f"  Bybit: {all_prices[4]}")

    # Преобразуем данные в читаемый формат (обрабатываем по парам)
    exchanges = ["Binance", "CoinMarketCap", "GateIO", "KuCoin", "Bybit"]
    for exchange, prices in zip(exchanges, all_prices):
        for pair, price_data in zip(pairs, prices):
            if price_data is None:
                logger.error(f"Нет данных для {pair} на {exchange}")
                continue

            # Текущая цена для пары
            current_price = Decimal(price_data)

            # Проверяем, есть ли предыдущая цена для этой пары на данной бирже
            if pair in last_prices[exchange]:
                last_price = last_prices[exchange][pair]
                # Рассчитываем процент изменения цены
                price_diff = (current_price - last_price) / last_price
                logger.info(f"{price_diff} {current_price}  {last_price}")
                # Если цена изменилась на >= 0.03%, отправляем email
                if abs(price_diff) >= 0:

                    total_amount = calculate_total_amount(
                        crypto_wallet, current_price, pair
                    )
                    # await send_email(pair, current_price, total_amount, price_diff)
                    send_email(
                        subject=f"Цена на {pair} выросла!",
                        body=(
                            f"Валютная пара: {pair}\n"
                            f"Текущая цена: {current_price}\n"
                            f"Последняя цена: {last_price}\n"
                            f"Разница: {price_diff:.4%}\n"
                            f"Стоимость накоплений: {total_amount} {pair[4:]}\n"
                            f"Дата: {datetime.now().isoformat()}"
                        ),
                        to="test@example.com",
                    )
                    # Логируем информацию
                    logger.info(
                        f"Цена на {pair} на {exchange} изменилась на {price_diff:.4%}. Отправлено уведомление."
                    )

                    await PriceRecord.save_price(
                        title=f"{exchange} {pair}",
                        price=current_price,
                        max_price=current_price,
                        min_price=last_price,
                        difference=price_diff,
                        total_amount=total_amount,
                    )
                    write_to_csv(
                        title=f"{exchange} {pair}",
                        price=current_price,
                        max_price=current_price,
                        min_price=last_price,
                        difference=price_diff,
                        total_amount=total_amount,
                    )

                    write_to_json(
                        title=f"{exchange} {pair}",
                        price=current_price,
                        max_price=current_price,
                        min_price=last_price,
                        difference=price_diff,
                        total_amount=total_amount,
                        coins={pair[:3]: pair[4:]},
                    )

            # Обновляем последнюю цену для пары на данной бирже
            last_prices[exchange][pair] = current_price

        # logger.info(f"Предыдущие цены на {exchange}: {last_prices[exchange]}")
        # logger.info(f"{last_prices}")


def calculate_total_amount(crypto_wallet, price, pair):
    # Пример расчета общей суммы с использованием переданного экземпляра
    total_amount = crypto_wallet.amount * price
    return total_amount
