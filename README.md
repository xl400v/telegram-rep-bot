# 🏆 Telegram-бот учёта активности и рейтинга участников

Современный Telegram-бот для геймификации и автоматизации учета турнирной рейтинга участников.

---

## 🚀 Установка и быстрый старт

1. Клонировать репозиторий
2. Установить зависимости: `pip install -r requirements.txt`
3. Настроить переменные окружения `.env`
4. Запустить: `python bot.py`


## 🚀 Установка и опытный старт `uv`

1. Установка интремента для работы с зависимостями `curl -LsSf https://astral.sh/uv/install.sh | sh`  
   В новом проекте необходимо установить зависимости `uv init --name bot_package`
2. Установить зависимости: `uv sync`
3. Настроить переменные окружения `.env`
4. **Запустить:** `uv run risebot`

### Настройка. Создайте в корне проекта файл `.env`

```env
LOG_LEVEL=WARNING
ADMIN_ID=
BOT_TOKEN=
DATABASE_URL=src/data/rasing.sqlite3
STAMP_NAME=AURON
```

### Команды

- `/start` - Запустить бота
- `/feedback` - Обратная связь
- `/join` - Присоединиться
- `/report` - Отправить отчет
- `/balance` - Рейтинг участников
- `/withdraw` - Вывод

## 📁 Структура проекта

```text
telegram-rep-bot/
├── .env                  # Переменные проекта
├── pyproject.toml        # Конфигурация проекта и зависимости
├── bot.py                # Точка входа (запуск)
└── src/
    ├── data/             # Папка для базы данных (будет монтироваться через Volume)
    │   └── sqlite3.db
    └── bot_package/      # Исходный код пакета
        ├── __init__.py   # Конфигурация (Settings)
        ├── database.py   # Работа с БД
        ├── handlers.py   # Обработчики команд
        └── main.py       # Основной цикл
```

## 🐳 Docker

```nix
docker build -t telegram-rep-bot .
```
```nix
docker run -d \
  --name risebot \
  --restart always \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  telegram-rep-bot
```