"""
попробовать мобильные прокси
"""

import logging
import traceback
import random
from playwright.async_api import async_playwright

# Конфигурация прокси
proxy_config = {
    "host": "45.130.70.221",
    "port": "8000",
    "username": "0EuSEE",
    "password": "oUd3gS",
}

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def smooth_mouse_move(page, start_x, start_y, end_x, end_y, steps=20):
    """
    Плавное перемещение мыши с разбивкой на шаги.
    """
    for i in range(steps):
        intermediate_x = start_x + (end_x - start_x) * (i / steps)
        intermediate_y = start_y + (end_y - start_y) * (i / steps)
        await page.mouse.move(intermediate_x, intermediate_y)
        await page.wait_for_timeout(50)  # Пауза между движениями для плавности


async def main():
    async with async_playwright() as playwright:
        # Запуск браузера с последними версиями Chromium
        browser = await playwright.chromium.launch(headless=False, slow_mo=250)

        # Создание нового контекста с прокси и пользовательскими параметрами
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="ru-RU",
            timezone_id="Europe/Moscow",
            geolocation={
                "longitude": 37.6173,
                "latitude": 55.7558,
            },  # Геолокация для Москвы
            permissions=["geolocation"],
            proxy={
                "server": f"http://{proxy_config['host']}:{proxy_config['port']}",
                "username": proxy_config["username"],
                "password": proxy_config["password"],
            },
            is_mobile=False,
        )

        # Добавление пользовательского скрипта для удаления атрибутов WebDriver и других проверок
        await context.add_init_script(
            """
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.navigator.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
            Object.defineProperty(navigator, 'languages', { get: () => ['ru-RU', 'ru'] });
        """
        )

        # Открытие новой страницы
        page = await context.new_page()

        # Логирование консольных сообщений и ошибок страницы
        page.on("console", lambda msg: logger.info(f"Console log: {msg.text}"))
        page.on("pageerror", lambda e: logger.error(f"Page error: {e}"))

        try:
            logger.info("Переход на страницу OZON...")
            await page.goto(
                "https://www.ozon.ru/", wait_until="networkidle", timeout=60000
            )

            # Ожидание появления кнопки с ID 'reload-button'
            await page.wait_for_selector("#reload-button", timeout=60000)
            logger.info("Кнопка 'Обновить' найдена")

            # Получение координат кнопки 'Обновить'
            button = await page.query_selector("#reload-button")
            bounding_box = await button.bounding_box()

            # Начальные координаты (например, из угла страницы)
            start_x, start_y = 0, 0

            # Смещаем точку клика от центра кнопки на случайные значения (например, на 5-15 пикселей)
            offset_x = random.randint(-15, 15)
            offset_y = random.randint(-15, 15)

            # Центр кнопки + случайное смещение
            target_x = bounding_box["x"] + bounding_box["width"] / 2 + offset_x
            target_y = bounding_box["y"] + bounding_box["height"] / 2 + offset_y

            # Плавное перемещение мыши на кнопку
            await smooth_mouse_move(page, start_x, start_y, target_x, target_y)
            logger.info(
                f"Мышь плавно наведена на кнопку 'Обновить' с координатами смещения ({offset_x}, {offset_y})"
            )

            # Пауза перед нажатием (эмуляция реального взаимодействия)
            await page.wait_for_timeout(500000000)

            # Эмуляция реального клика: нажать и отпустить левую кнопку мыши
            await page.mouse.down()
            await page.wait_for_timeout(
                100
            )  # Немного подождать между нажатием и отпусканием
            await page.mouse.up()

            logger.info("Нажатие на кнопку 'Обновить' выполнено")

        except Exception as e:
            logger.error(f"Ошибка при работе со страницей: {e}")
            logger.error(f"Полная трассировка: {traceback.format_exc()}")

        # Закрытие браузера
        await browser.close()


# Запуск скрипта
if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
