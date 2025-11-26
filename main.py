# main.py
import telebot
from config import TELEGRAM_BOT_TOKEN, BOT_NAME
from db import init_db, create_user_if_not_exists, get_user
import start_handler, lesson_handler, quiz_handler, voice_handler, shop_handler, progress_handler
import keyboards

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN, parse_mode="HTML")

def register_all():
    start_handler.register(bot)
    lesson_handler.register(bot)
    quiz_handler.register(bot)
    voice_handler.register(bot)
    shop_handler.register(bot)
    progress_handler.register(bot)

if __name__ == "__main__":
    print("Initializing DB...")
    init_db()
    print(f"Starting {BOT_NAME}...")
    register_all()
    bot.infinity_polling()