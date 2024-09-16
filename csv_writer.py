import csv
from datetime import datetime


def write_to_csv(data, filename="prices.csv"):
    header = [
        "title",
        "price",
        "max price",
        "min price",
        "date",
        "difference",
        "total amount",
    ]
    with open(filename, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        if file.tell() == 0:  # Записываем заголовок только если файл пустой
            writer.writeheader()
        for row in data:
            writer.writerow(row)
