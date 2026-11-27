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
   В новом проекте необходимо установить зависимости `uv init --name MensRise_bot` && `uv add python-dotenv python-telegram-bot`
2. Установить зависимости: `uv sync`
3. Настроить переменные окружения `.env`
4. Запустить: `uv run bot.py`

### Настройка. Создайте в корне проекта файл `.env`

```env
ADMIN_ID=
BOT_TOKEN=
DATABASE_URL=rasing.sqlite3
STAMP_NAME=AURON
```

### Команды

- `/start` - Запустить бота
- `/feedback` - Обратная связь
- `/join` - Присоединиться
- `/report` - Отправить отчет
- `/balance` - Рейтинг участников
- `/withdraw` - Вывод

## 🐳 Docker

```nix
docker run -d \
  --name mensrise_bot \
  --restart always \
  --env-file .env \
  -v /home/user/bot_data:/app/data \
  telegram-rep-bot
```