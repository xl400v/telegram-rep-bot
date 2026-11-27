# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы конфигурации зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости в системный Python (для упрощения запуска в контейнере)
# --system позволяет не создавать виртуальное окружение внутри контейнера, 
# так since контейнер сам по себе является изолированной средой.
RUN uv pip install --system --no-cache -r pyproject.toml

# Копируем весь остальной код проекта
COPY . .

# Создаем папку для данных (базы данных)
# Важно: путь должен совпадать с тем, что вы будете монтировать через Volume
RUN mkdir -p /app/data

# Указываем переменную окружения, чтобы бот знал, где искать БД
# Если в .env указано 'rasing.sqlite3', путь станет '/app/rasing.sqlite3'
#ENV DATABASE_URL=/app/src/data/rasing.sqlite3

# Запускаем бота напрямую через python
CMD ["uv", "run", "risebot"]