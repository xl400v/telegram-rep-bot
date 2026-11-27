import logging, datetime
from telegram.error import TimedOut
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from bot_package import handlers, database, config as ENV  # Импорт из __init__.py

logging.basicConfig(level=ENV.log_level)

if not ENV.bot_token:
    logging.critical("\033[91m ОШИБКА: BOT_TOKEN не найден в файле .env!\033[0m")

def main():
    database.init()
    app = Application.builder().token(ENV.bot_token).build()

    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("join", handlers.join))
    app.add_handler(CommandHandler("balance", handlers.balance))
    app.add_handler(CommandHandler("report", handlers.report))
    app.add_handler(CommandHandler("withdraw", handlers.withdraw))
    app.add_handler(CommandHandler("feedback", handlers.feedback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.handle_message))

    try:
        logging.warning("\033[92m==== [%s] BOT STARTED ====\033[0m", datetime.datetime.now().strftime("%H:%M:%S"))
        app.run_polling()
    except TimedOut as e:
        logging.critical("\033[91m Не удалось установить соединение с Telegram (СЕТЕВАЯ ОШИБКА: %s). Проверьте интернет или прокси.\033[0m", e)
    except Exception as e:
        logging.error("\033[91m НЕПРЕДВИДЕННАЯ ОШИБКА:\033[0m%s", e)

if __name__ == "__main__":
    main()