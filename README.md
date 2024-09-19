# PriceMonitor
![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat&logo=python)
![Playwright](https://img.shields.io/badge/Playwright-1.47.0-green?style=flat&logo=microsoft-edge)
![Asyncio](https://img.shields.io/badge/Asyncio-3.4.3-orange?style=flat&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue?style=flat&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-20.10-blue?style=flat&logo=docker)
![Tortoise ORM](https://img.shields.io/badge/Tortoise%20ORM-0.21.6-green?style=flat&logo=python)
![Mailcatcher](https://img.shields.io/badge/Mailcatcher-1080-orange?style=flat&logo=mailcatcher)
![aiohttp](https://img.shields.io/badge/aiohttp-3.10.5-blue?style=flat&logo=aiohttp)
![black](https://img.shields.io/badge/black-24.8.0-black?style=flat&logo=python)

## Описание

**PriceMonitor** — это проект, который автоматически мониторит цены на товары с различных маркетплейсов (например, Yandex Market и Wildberries), а также следит за курсами криптовалют с нескольких бирж. Проект использует асинхронные технологии, такие как `asyncio` и `Playwright`, для обработки данных с минимальными задержками. Результаты сохраняются в базе данных PostgreSQL, а уведомления отправляются через Mailcatcher.

## Функциональность
- Парсинг цен криптовалют с нескольких бирж:

    ●   https://www.binance.com

    ●   https://coinmarketcap.com

    ●   https://www.bybit.com

    ●   https://www.gate.io

    ●   https://www.kucoin.com

- Мониторинг цен на товары с маркетплейсов.

- Асинхронная обработка данных с использованием `asyncio`.
- Отправка уведомлений об измении цены на пороговое значение через Mailcatcher.
- Использование PostgreSQL и Tortoise ORM  для хранения данных о ценах.

 ## Установка и запуск

1. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/maksorli/PriceMonitor.git
   cd PriceMonitor

2. Проверьте версию Docker и Docker Compose, либо установите:
    ```bash
    docker --version
    docker-compose --version
3. Заполните файл .env  с переменными окружения
    ```bash
    #api key для coinmarketcap
    COINMARKETCAP_API_KEY ='122122-2222-222-82226c-33' 

    #путь в бд
    db_path="postgres://pricemonitor:password@localhost:5432/pricemonitor"  

    #список товаров для поиска
    goods="копье,дуршлаг,красные носки,леска для спиннинга"

    #частота запроса к биржам в секундах
    crypto_frequency = '90' 

    #частота запроса к маркетлейсам в секундах
    mp_frequency = '10'   

    #порог разницы цен
    crypto_threshold = '0.0003' 


3. Запустите проект с помощью Docker Compose:
   ```bash
   docker-compose up --build
4. Откройте Mailcatcher для проверки отправленных писем:
    http://localhost:1080
5. Для управления базой данных PostgreSQL:
    docker exec -it postgres_db psql -U pricemonitor pricemonitor

    ## Переменные окружения файл. необходимо заполнить файл .env
    
