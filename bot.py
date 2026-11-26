import sqlite3, os, logging, datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.error import TimedOut
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

logging.basicConfig(level=logging.WARNING)
load_dotenv()

ADMIN_ID = int(os.getenv('ADMIN_ID'))
BOT_TOKEN = os.getenv('BOT_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')

if not BOT_TOKEN:
    logging.critical("\033[91m ОШИБКА: BOT_TOKEN не найден в файле .env!\033[0m")

# ---------------- DB ----------------
conn = sqlite3.connect(DATABASE_URL, check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0
)
""")
conn.commit()

# ---------------- STATES ----------------
state = {}

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.warning("\033[94m START ID: \033[0m%s", update.effective_user.id)
    await update.message.reply_text(
        "🌅 Добро пожаловать в проект «СОБР»\n\n"
        "Команды:\n"
        "/join — присоединиться\n"
        "/balance — баланс\n"
        "/report — отчёт\n"
        "/withdraw — вывод\n"
        "/feedback — обратная связь"
    )

# ---------------- JOIN ----------------
async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    cur.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    if cur.fetchone():
        await update.message.reply_text("Вы уже участник ⚡")
        return
        
    cur.execute("INSERT INTO users (user_id, balance) VALUES (?, 0)", (user_id,))
    conn.commit()

    logging.warning("\033[92m NEW ID: \033[0m%s", user_id)
    await update.message.reply_text("Вы присоединились к проекту 🌅")

# ---------------- BALANCE ----------------
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    cur.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    
    if not row:
        await update.message.reply_text("Сначала /join")
        return
        
    await update.message.reply_text(f"💰 Баланс: {row[0]} AURON")

# ---------------- REPORT ----------------
async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.warning("\033[94m REPORT TRIGGER\033[0m")
    state[update.effective_user.id] = "report"
    await update.message.reply_text("Отправьте текст отчёта одним сообщением:")

# ---------------- WITHDRAW ----------------
async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state[update.effective_user.id] = "withdraw"
    await update.message.reply_text("Введите сумму (минимум 1000):")

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    state[user_id] = "feedback"
    
    await update.message.reply_text(
        "✍️ Напишите ваш вопрос в поддержку одним сообщением:"
    )
    
# ---------------- ADMIN HELPERS ----------------
async def send_to_admin(text):
    # helper функция
    return text

# ---------------- MESSAGE HANDLER (ЕДИНЫЙ) ----------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.warning("\033[92m HANDLE MESSAGE ID: \033[0m%s", update.message.message_id)
    user_id = update.effective_user.id
    text = update.message.text
    current_state = state.get(user_id)

    # ---------------- REPORT ----------------
    if current_state == "report":
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📩 ОТЧЁТ\nUser: {user_id}\nText: {text}"
        )

        await update.message.reply_text("Отчёт отправлен ⚡")
        state.pop(user_id, None)
        return

    # ---------------- WITHDRAW AMOUNT ----------------
    if current_state == "withdraw":
        if not text.isdigit():
            await update.message.reply_text("Введите число")
            return
            
        amount = int(text)
        
        if amount < 1000:
            await update.message.reply_text("Минимум 1000 AURON")
            state.pop(user_id, None)
            return
        
        cur.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
        row = cur.fetchone()
        
        if not row or amount > row[0]:
            await update.message.reply_text("Недостаточно средств ❌")
            state.pop(user_id, None)
            return
        
        state[user_id] = f"wallet:{amount}"
        await update.message.reply_text("Введите адрес кошелька:")
        return

    # ---------------- WITHDRAW WALLET ----------------
    if current_state and current_state.startswith("wallet:"):
        amount = int(current_state.split(":")[1])
        wallet = text
        
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                "💸 ВЫВОД СРЕДСТВ\n\n"
                f"User: {user_id}\n"
                f"Amount: {amount}\n"
                f"Wallet: {wallet}"
            )
        )
        
        await update.message.reply_text("Данная функция временно недоступна❌")
        state.pop(user_id, None)
        return

    # ---------------- FEEDBACK ----------------
    if current_state == "feedback":
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                "📨 ОБРАТНАЯ СВЯЗЬ\n\n"
                f"User ID: {user_id}\n"
                f"Message: {text}"
            )
        )
        
        await update.message.reply_text("Сообщение отправлено в поддержку ⚡")
        state.pop(user_id, None)
        return

# ---------------- MAIN ----------------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("join", join))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("withdraw", withdraw))
    app.add_handler(CommandHandler("feedback", feedback))

    # ВАЖНО: только один MessageHandler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    try:
        logging.warning("\033[92m==== [%s] BOT STARTED ====\033[0m", datetime.datetime.now().strftime("%H:%M:%S"))
        # Пытаемся запустить опрос серверов Telegram
        app.run_polling()
    except TimedOut as e:
        # Логируем ошибку тайм-аута (сетевое соединение не установлено)
        logging.critical("\033[91m Не удалось установить соединение с Telegram (СЕТЕВАЯ ОШИБКА: %s). Проверьте интернет или прокси.\033[0m", e)
    except Exception as e:
        # Логируем любые другие непредвиденные ошибки
        logging.error("\033[91m НЕПРЕДВИДЕННАЯ ОШИБКА:\033[0m%s", e)

if __name__ == "__main__":
    main()