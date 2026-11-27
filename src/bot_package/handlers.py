import logging
from telegram import Update
#from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from bot_package import database, config as ENV  # Импорт из __init__.py

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.warning("\033[94m START ID: \033[0m%s", update.effective_user.id)
    await update.message.reply_text("🌅 Добро пожаловать в проект «СОБР»")

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id  
    database.cur.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    if database.cur.fetchone():
        await update.message.reply_text("Вы уже участник ⚡")
        return  
    database.add_user(user_id)

    logging.warning("\033[92m NEW ID: \033[0m%s", user_id)
    await update.message.reply_text("🌅 Вы присоединились к проекту")

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    database.cur.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
    if not database.cur.fetchone():
        await update.message.reply_text("Сначала /join")
        return
    context.user_data['state'] = "report"

    logging.warning("\033[94m REPORT TRIGGER\033[0m")
    await update.message.reply_text("Отправьте текст отчёта (<i>одним сообщением</i>):", parse_mode="HTML")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id  
    row = database.get_user_balance(user_id)
    if not row:
        await update.message.reply_text("Сначала /join")
        return  
    await update.message.reply_text(f"💰 Баланс: {row[0]} {ENV.stamp_name}")

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id  
    row = database.get_user_balance(user_id)
    if not row:
        await update.message.reply_text("Сначала /join")
        return
    context.user_data['state'] = "withdraw"
    await update.message.reply_text("Введите сумму (минимум 1000):")  

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['state'] = "feedback"  
    await update.message.reply_text("✍️ Напишите ваш вопрос в поддержку одним сообщением:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    fullname = await context.bot.get_chat(user_id)
    text = update.message.text
    state = context.user_data.get('state')
    logging.warning("\033[92m HANDLE MESSAGE [%s] FROM ID %s: \033[0m%s", update.message.message_id, user_id, text)

    if state == "report":
        await context.bot.send_message(chat_id=ENV.admin_id, text=f"📩 ОТЧЁТ #id{user_id}\nUser: {fullname.first_name}\n\nText: {text}")
        await update.message.reply_text("Отчёт отправлен ⚡")
        context.user_data.pop('state', None)

    elif state == "withdraw":
        if not text.isdigit():
            await update.message.reply_text("Введите число")
            return
        least = 1000
        amount = int(text)
        if amount < least:
            await update.message.reply_text(f"<u>Минимум {least} {ENV.stamp_name}</u>", parse_mode="HTML")
            context.user_data.pop('state', None)
            return
        
        row = database.get_user_balance(user_id)
        if not row or amount > row[0]:
            await update.message.reply_text("Недостаточно средств ❌")
            context.user_data.pop('state', None)
            return
        
        context.user_data['wallet_amount'] = amount
        context.user_data['state'] = "wallet_waiting"
        await update.message.reply_text("Введите адрес кошелька:")

    elif state == "wallet_waiting":
        amount = context.user_data.get('wallet_amount')
        await context.bot.send_message(chat_id=ENV.admin_id, text=f"💸 ВЫВОД #id{user_id}\nUser: {fullname.first_name}\nAmount: {amount}\nWallet: {text}")
        await update.message.reply_text("Данная функция временно недоступна ❌")
        #database.set_user_balance(user_id, -10)
        context.user_data.pop('state', None)

    elif state == "feedback":
        await context.bot.send_message(chat_id=ENV.admin_id, text=f"📨 ОБРАТНАЯ СВЯЗЬ #id{user_id}\nUser: {fullname.first_name}\n\nMsg: {text}")
        await update.message.reply_text("Сообщение отправлено в поддержку ⚡")
        context.user_data.pop('state', None)