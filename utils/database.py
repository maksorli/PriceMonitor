import logging
import os
from tortoise import fields, Tortoise
from tortoise.models import Model
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()

logger = logging.getLogger(__name__)


class PriceRecord(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    price = fields.DecimalField(max_digits=15, decimal_places=8)
    max_price = fields.DecimalField(max_digits=15, decimal_places=8)
    min_price = fields.DecimalField(max_digits=15, decimal_places=8)
    date = fields.DatetimeField(auto_now_add=True)
    difference = fields.DecimalField(max_digits=5, decimal_places=4)
    total_amount = fields.DecimalField(max_digits=15, decimal_places=8)


class MP_PriceRecord(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    price = fields.DecimalField(max_digits=15, decimal_places=8)
    max_price = fields.DecimalField(max_digits=15, decimal_places=8)
    description = fields.CharField(max_length=1000)
    min_price = fields.DecimalField(max_digits=15, decimal_places=8)
    date = fields.DatetimeField(auto_now_add=True)

    @classmethod
    async def save_price(
        cls,
        title: str,
        price: Decimal,
        max_price: Decimal,
        min_price: Decimal,
        difference: Decimal,
        total_amount: Decimal,
    ) -> None:
        """Сохраняет запись в таблицу PriceRecord."""
        try:
            await cls.create(
                title=title,
                price=price,
                max_price=max_price,
                min_price=min_price,
                difference=difference,
                total_amount=total_amount,
            )
            logger.info("Данные успешно сохранены в базу")
        except Exception as e:
            logger.error(f"Ошибка при сохранении данных: {e}")

    @classmethod
    async def mp_save_price(
        cls,
        title: str,
        price: Decimal,
        max_price: Decimal,
        min_price: Decimal,
        description: str,
    ) -> None:
        """Сохраняет запись в таблицу PriceRecord."""
        try:
            await cls.create(
                title=title,
                price=price,
                max_price=price,
                min_price=price,
                description=description or "Описание недоступно",
            )
            logger.info("Данные успешно сохранены в базу")
        except Exception as e:
            logger.error(f"Ошибка при сохранении данных: {e}")


async def init_db() -> None:
    """Инициализация базы данных."""
    await Tortoise.init(
        db_url=os.getenv("db_path"),
        modules={"models": ["utils.database"]},
    )
    await Tortoise.generate_schemas()
