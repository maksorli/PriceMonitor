import json
import os
from decimal import Decimal
from datetime import datetime


def write_to_json(title, price, max_price, min_price, difference, total_amount, coins):
    # Структура JSON
    key_json = {
        "title": title,
        "kash": [
            {
                "price": float(
                    price
                ),  # Преобразуем Decimal в float для сериализации в JSON
                "minmax": [
                    {"max price": float(max_price), "min price": float(min_price)}
                ],
            }
        ],
        "difference": float(difference),  # Преобразуем Decimal в float
        "total amount": float(total_amount),  # Преобразуем Decimal в float
        "coins": coins,  # Список валют
        "date": datetime.now().isoformat(),  # Дата в формате ISO
    }

    file_path = "liquorice.json"

    # Проверяем, существует ли файл
    if os.path.exists(file_path):
        # Если файл существует, загружаем его содержимое
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
    else:
        # Если файла нет, создаем пустой список данных
        data = []

    # Добавляем новые данные в существующий список
    data.append(key_json)

    # Записываем обновленные данные в JSON-файл
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
