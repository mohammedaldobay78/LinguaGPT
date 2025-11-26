# start_handler.py
from telebot.types import Message
import keyboards, db
from config import BOT_NAME

def register(bot):
    @bot.message_handler(commands=["start"])
    def start(m: Message):
        user_id = m.from_user.id
        username = m.from_user.username or m.from_user.first_name or str(user_id)
        db.create_user_if_not_exists(user_id, username)
        user = db.get_user(user_id)

        intro = (
            f"أهلاً بك في <b>{BOT_NAME}</b> 🤖\n\n"
            "أنا مساعدك لتعلم الإنجليزية بالذكاء الاصطناعي.\n"
            "- أشرح دروساً مخصّصة عبر AI\n"
            "- اختبارات عبر Poll\n"
            "- تحسين نطق (بعد الشراء)\n\n"
            "اختر من القائمة للبدء."
        )
        bot.send_message(user_id, intro, reply_markup=keyboards.main_menu())

    @bot.message_handler(func=lambda m: m.text == "عودة ⤴️")
    def back(m: Message):
        bot.send_message(m.chat.id, "القائمة الرئيسية:", reply_markup=keyboards.main_menu())