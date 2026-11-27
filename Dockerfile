FROM python:3.12-slim

# Устанавливаем uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Копируем файлы конфигурации
COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости
RUN uv sync --frozen --no-install-project --system

# Копируем код
COPY . .

# СОЗДАЕМ ПАПКУ ДЛЯ ДАННЫХ
RUN mkdir -p /app/data

CMD ["uv", "run", "bot.py"]