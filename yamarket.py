from playwright.async_api import async_playwright

import logging
import re

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
import asyncio
from proxy_list import proxy_config


goods = ["копье", "дуршлаг", "красные носки", "леска для спиннинга"]


async def yandex_market(search_term, proxy_config):

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=False,
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

        await page.goto("https://market.yandex.ru/", wait_until="domcontentloaded")

        await page.fill('input[name="text"]', search_term)

        await page.press('input[name="text"]', "Enter")

        await page.wait_for_load_state("load")
        await page.wait_for_selector('button[data-autotest-id="aprice"]')
        logger.info("Кнопка 'подешевле' найдена")

        # Проверка состояния кнопки перед кликом
        button = await page.query_selector('button[data-autotest-id="aprice"]')

        if await button.get_attribute("aria-pressed") != "true":
            # Кликаем по кнопке только если она еще не нажата
            await page.click('button[data-autotest-id="aprice"]')
            logger.info("Клик по кнопке 'подешевле' выполнен, ожидаем 5 сек")
            await page.wait_for_timeout(5000)

        else:
            logger.info("Кнопка 'подешевле' уже нажата, повторного клика не требуется")

        # Находим все элементы с data-apiary-widget-name="@light/Organic"
        organic_element = await page.query_selector(
            '[data-apiary-widget-name="@light/Organic"]'
        )

        # Проверяем, найден ли элемент
        if organic_element:
            # Находим первую ссылку внутри этого блока
            product_links = await organic_element.query_selector_all(
                'a[data-auto="snippet-link"]'
            )

            if product_links and len(product_links) > 0:
                # Извлекаем первую ссылку
                href = "https://market.yandex.ru" + await product_links[
                    0
                ].get_attribute("href")

                # Открываем новую вкладку и переходим по ссылке
                new_page = await context.new_page()
                await new_page.goto(href, wait_until="load")
                await page.wait_for_timeout(2000)
                product_name_element = await new_page.query_selector(
                    'h1[data-auto="productCardTitle"]'
                )

                # Извлекаем текстовое содержимое
                if product_name_element:
                    product_name = await product_name_element.inner_text()
                    print(f"Название товара: {product_name}")
                else:
                    print("Название товара не найдено.")

                # Ищем элемент с ценой товара по атрибуту 'data-auto="snippet-price-current"'
                price_element = await new_page.query_selector(
                    'h3[data-auto="snippet-price-current"]'
                )

                # Извлекаем текстовое содержимое
                if price_element:
                    price_text = await price_element.inner_text()
                    price = re.sub(r"\D", "", price_text)
                    print(f"Цена товара: {price}")
                else:
                    print("Цена товара не найдена.")

                description_element = await new_page.query_selector(
                    'div[aria-label="product-description"]'
                )
                if description_element:
                    description = await description_element.inner_text()
                    print(f"Описание товара: {description}")
                else:
                    print("Описание товара не найдено.")

                await new_page.wait_for_timeout(5000)
            else:
                print("Ссылки не найдены в блоке.")
        else:
            print("Элемент с data-apiary-widget-name='@light/Organic' не найден.")

        await browser.close()


async def main():
    # Запускаем задачи параллельно
    await asyncio.gather(*(yandex_market(good, proxy_config) for good in goods))


# Запуск программы
asyncio.run(main())
