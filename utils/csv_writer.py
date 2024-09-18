import csv
from datetime import datetime
import os


def write_to_csv(title, price, max_price, min_price, difference, total_amount):
    # Заголовки таблицы (если файл пустой)
    header = [
        "title",
        "price",
        "max price",
        "min price",
        "date",
        "difference",
        "total amount",
    ]
    file_path = "liquorice.csv"

    # Проверяем, существует ли файл
    file_exists = os.path.isfile(file_path)
    with open(file_path, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(header)
        date_iso = datetime.now().isoformat()  # Текущая дата и время в формате ISO
        writer.writerow(
            [title, price, max_price, min_price, date_iso, difference, total_amount]
        )
