def pair_dict(all_prices):
    """
    Собираем список по валютным парам
    """
    all_pairs_prices = []
    pairs = [
        "BTC/USDT",
        "ETH/BTC",
        "XMR/BTC",
        "SOL/BTC",
        "BTC/RUB",
        "DOGE/BTC",
    ]  # порядок пар
    for i, pair in enumerate(pairs):
        prices_for_pair = []
        for prices in all_prices:
            if prices is not None and i < len(prices):
                prices_for_pair.append(prices[i])  # Добавляем цену для пары
            else:
                prices_for_pair.append(None)  # Если данных нет, добавляем None
        all_pairs_prices.append(prices_for_pair)
    return all_pairs_prices
