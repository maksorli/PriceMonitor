from playwright.async_api import async_playwright
from playwright.async_api import TimeoutError

import logging
import re

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import asyncio
from proxy_list import proxy_config
from utils.database import MP_PriceRecord, init_db


goods = ["копье", "дуршлаг", "красные носки", "леска для спиннинга"]


async def wildberries(search_term, proxy_config):

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=True,
            proxy={
                "server": f"http://{proxy_config['host']}:{proxy_config['port']}",
                "username": proxy_config["username"],
                "password": proxy_config["password"],
            },
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.138 Safari/537.36"
        )

        page = await context.new_page()
        try:
            await page.goto(
                "https://www.wildberries.ru/", wait_until="load", timeout=60000
            )
        except TimeoutError:
            logger.error("Превышено время ожидания загрузки страницы.")
             
            return None
        await page.fill("#searchInput", search_term)

        await page.press("#searchInput", "Enter")

        await page.wait_for_load_state("load")
        try:
            await page.wait_for_selector(
                "button.dropdown-filter__btn--sorter", timeout=60000
            )  # Ждем появления кнопки
        except:
            logger.info("ошибка загрузки страницы")
            await browser.close()
        await page.click("button.dropdown-filter__btn--sorter")  # Нажимаем на кнопку
        await page.wait_for_timeout(2000)

        await page.click("text=По возрастанию цены")  # Кликаем по тексту элемента
        await page.wait_for_timeout(2000)
        # Получаем href из первого элемента
        href = await page.get_attribute(
            "a.product-card__link.j-card-link.j-open-full-product-card", "href"
        )
        # Выводим ссылку
        logger.info(f"Ссылка на продукт: {href}")
        # Открываем новую вкладку и переходим по ссылке
        new_page = await context.new_page()
        await new_page.goto(href, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)

        # ищем название
        try:
            product_name = await new_page.text_content("h1.product-page__title")

            logger.info(f"{product_name} найден")
        except:
            logger.info("product_name_element не найден")
            product_name = "названия не найдено"
        # ищем цену
        try:
            price_text = await new_page.text_content(
                "span.price-block__wallet-price", timeout=1000
            )
            price = re.sub(r"\D", "", price_text)
            logger.info(f"{price} найден")
        except:
            logger.info("price не найден")
            price = 0

        try:
            price_text = await new_page.text_content(
                "ins.price-block__final-price.red-price", timeout=1000
            )
            price = re.sub(r"\D", "", price_text)
            logger.info(f"{price} найден")
        except:
            logger.info("price не найден")
            price = 0

        await MP_PriceRecord.mp_save_price(
            title=product_name,
            price=price,
            max_price=price,
            min_price=price,
            marketplace="Wildberries",
            description="описание отсутствует",
            link=href,
        )

        logger.info("парсинг успешно завершен.")

        await browser.close()
