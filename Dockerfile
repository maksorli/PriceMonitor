# Используем образ Python
FROM python:3.10-slim

# Используем образ Python
FROM python:3.10-slim

# Установка Node.js и npm для Playwright
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean

# Установка зависимостей для Playwright
RUN apt-get update && apt-get install -y \
    libnss3 libatk-bridge2.0-0 libxcomposite1 libxrandr2 libxdamage1 libxkbcommon0 libgtk-3-0 libgbm-dev libpango-1.0-0 \
    && apt-get clean

# Установка Playwright зависимостей
RUN npx playwright install-deps
# Установка зависимостей для работы с PostgreSQL
RUN pip install --upgrade pip
RUN pip install psycopg2-binary

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости проекта из requirements.txt, включая Playwright
RUN pip install -r requirements.txt

# Устанавливаем необходимые браузеры для Playwright
RUN playwright install

# Копируем скрипт wait-for-it.sh и код приложения
COPY wait-for-it.sh /app/wait-for-it.sh
COPY . /app

# Делаем wait-for-it.sh исполняемым
RUN chmod +x /app/wait-for-it.sh

WORKDIR /app

# Указываем команду для запуска парсинга
CMD ["python", "main.py"]
