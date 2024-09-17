from tortoise import fields, Tortoise
from tortoise.models import Model
import os
from dotenv import load_dotenv

load_dotenv()


class PriceRecord(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    price = fields.DecimalField(max_digits=15, decimal_places=8)
    max_price = fields.DecimalField(max_digits=15, decimal_places=8)
    min_price = fields.DecimalField(max_digits=15, decimal_places=8)
    date = fields.DatetimeField(auto_now_add=True)
    difference = fields.DecimalField(max_digits=5, decimal_places=4)
    total_amount = fields.DecimalField(max_digits=15, decimal_places=8)


async def init_db():
    await Tortoise.init(
        db_url=os.getenv("db_path"),
        modules={"models": ["database"]},
    )
    await Tortoise.generate_schemas()


async def save_price(data):
    await PriceRecord.create(**data)


async def get_price_records():
    return await PriceRecord.all()
