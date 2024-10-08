from playwright.async_api import async_playwright
import logging
import re
from playwright.async_api import TimeoutError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
from utils.database import MP_PriceRecord


async def yandex_market(search_term, proxy_config=None):

    async with async_playwright() as p:
        if proxy_config:
            browser = await p.chromium.launch(
                headless=True,
                proxy={
                    "server": f"http://{proxy_config['host']}:{proxy_config['port']}",
                    "username": proxy_config["username"],
                    "password": proxy_config["password"],
                },
            )
        else:
            browser = await p.chromium.launch(headless=True)

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.138 Safari/537.36"
        )

        page = await context.new_page()
        try:
            logger.error(
                "открываю страницу https://market.yandex.ru/, таймаут 90 секунд"
            )
            await page.goto(
                "https://market.yandex.ru/", wait_until="load", timeout=90000
            )
        except TimeoutError:
            logger.error(
                "Превышено время ожидания загрузки страницы. https://market.yandex.ru/"
            )
            return
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
        logger.info("organic_element  найден")
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
                await new_page.goto(href, wait_until="domcontentloaded")
                await page.wait_for_timeout(2000)
                try:
                    product_name_element = await new_page.query_selector(
                        'h1[data-auto="productCardTitle"]'
                    )
                    logger.info("product_name_element найден")
                except:
                    logger.info("product_name_element не найден")

                # Извлекаем текстовое содержимое
                if product_name_element:
                    product_name = await product_name_element.inner_text()
                    logger.info(f"Название товара: {product_name}")
                else:
                    logger.info("Название товара не найдено.")

                # Ищем элемент с ценой товара по атрибуту 'data-auto="snippet-price-current"'
                price_element = await new_page.query_selector(
                    'h3[data-auto="snippet-price-current"]'
                )

                # Извлекаем текстовое содержимое
                if price_element:
                    price_text = await price_element.inner_text()
                    price = re.sub(r"\D", "", price_text)
                    logger.info(f"Цена товара: {price}")
                else:
                    logger.info("Цена товара не найдена.")

                description_element = await new_page.query_selector(
                    'div[aria-label="product-description"]'
                )
                if description_element:
                    description = await description_element.inner_text()
                    logger.info(f"Описание товара: {description}")
                else:
                    description = "описание отсутствует"
                    logger.info("Описание товара не найдено.")

                await new_page.wait_for_timeout(5000)
            else:
                logger.info("Ссылки не найдены в блоке.")
        else:
            logger.info("Элемент с data-apiary-widget-name='@light/Organic' не найден.")

        # пишем в бд
        await MP_PriceRecord.mp_save_price(
            title=product_name,
            price=price,
            max_price=price,
            min_price=price,
            description=description,
            marketplace="Yandex Market",
            link=href,
        )

        logger.info("парсинг успешно завершен.")
        await browser.close()
