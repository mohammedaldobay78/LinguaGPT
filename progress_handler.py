# progress_handler.py
from telebot.types import Message
import db, keyboards

def register(bot):
    @bot.message_handler(func=lambda m: m.text == "📊 تقدمي")
    def progress(m: Message):
        user_id = m.chat.id
        u = db.get_user(user_id)
        if not u:
            bot.send_message(user_id, "سجّل أولًا باستخدام /start")
            return
        txt = (
            f"📊 تقدمك:\n"
            f"المستوى: {u.get('level')}\n"
            f"الوحدة: {u.get('unit')}\n"
            f"الدروس المكتملة: {u.get('lessons_completed')}\n"
            f"Coins: {u.get('coins')}\n"
            f"Pronunciation VIP: {'نعم' if u.get('vip_pronunciation') else 'لا'}"
        )
        bot.send_message(user_id, txt, reply_markup=keyboards.main_menu())