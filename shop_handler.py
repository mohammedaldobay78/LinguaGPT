# shop_handler.py
from telebot.types import Message
import db, keyboards, config, time

def register(bot):
    @bot.message_handler(func=lambda m: m.text == "🛒 المتجر")
    def shop_entry(m: Message):
        bot.send_message(m.chat.id, "قائمة المتجر:", reply_markup=keyboards.shop_menu())

    @bot.message_handler(func=lambda m: m.text.startswith("شراء:"))
    def handle_buy(m: Message):
        user_id = m.chat.id
        text = m.text
        # map button text to item keys
        mapping = {
            "شراء: رفع مستوى A (5)": "upgrade_a",
            "شراء: رفع مستوى B (5)": "upgrade_b",
            "شراء: رفع الكويزات (8)": "boost_quizzes",
            "شراء: فتح تصحيح النطق (25)": "pronunciation_ai",
            "شراء: learning 24h (50)": "learning_24h"
        }
        item = mapping.get(text)
        if not item:
            bot.send_message(user_id, "عنصر غير معروف.")
            return
        price = config.SHOP_ITEMS.get(item, 99999)
        u = db.get_user(user_id)
        if not u:
            bot.send_message(user_id, "سجّل أولاً باستخدام /start")
            return
        if u['coins'] < price:
            bot.send_message(user_id, f"ليس لديك ما يكفي من coins. لديك: {u['coins']}, سعر العنصر: {price}")
            return
        ok = db.spend_coins(user_id, price)
        if not ok:
            bot.send_message(user_id, "فشل الشراء.")
            return
        # apply item
        if item == "upgrade_a":
            db.update_user_field(user_id, 'upgrade_a', 1)
        elif item == "upgrade_b":
            db.update_user_field(user_id, 'upgrade_b', 1)
        elif item == "boost_quizzes":
            db.update_user_field(user_id, 'boost_quizzes', 1)
        elif item == "pronunciation_ai":
            db.update_user_field(user_id, 'vip_pronunciation', 1)
        elif item == "learning_24h":
            # set learning_24h_until to now + big period (e.g., 24h from now)
            db.update_user_field(user_id, 'learning_24h_until', int(time.time()) + 24*3600)
        db.record_purchase(user_id, item)
        bot.send_message(user_id, f"تم شراء {config.SHOP_NAMES.get(item,item)} بنجاح. رصيدك الآن: {db.get_user(user_id)['coins']}")