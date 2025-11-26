# lesson_handler.py
from telebot.types import Message
import ai, db, keyboards, time
from config import DAILY_LESSON_SECONDS, COIN_REWARD, LEVELS

def register(bot):
    @bot.message_handler(func=lambda m: m.text == "📘 الدروس")
    def enter(m: Message):
        bot.send_message(m.chat.id, "قائمة الدروس:", reply_markup=keyboards.lesson_menu())

    @bot.message_handler(func=lambda m: m.text == "ابدأ درس اليوم ▶️")
    def start_lesson(m: Message):
        user_id = m.chat.id
        u = db.get_user(user_id)
        if not u:
            bot.send_message(user_id, "خطأ: سجل أولاً باستخدام /start")
            return

        # check if already started and not expired, or if learning24h purchased
        now = int(time.time())
        start_ts = db.get_lesson_session_start(user_id)
        learning24_until = u.get('learning_24h_until',0)
        if learning24_until and learning24_until > now:
            allowed = True
        else:
            allowed = False
            if start_ts == 0:
                allowed = True
            else:
                elapsed = now - start_ts
                if elapsed >= DAILY_LESSON_SECONDS:
                    # session expired
                    bot.send_message(user_id, f"عزيزي {u.get('username','')}, لقد انتهت الدروس لهذا اليوم نراك غداً\nأو اشتري ميزة (learning 24h) من المتجر")
                    db.end_lesson_session(user_id)
                    return
                else:
                    remaining = DAILY_LESSON_SECONDS - elapsed
                    bot.send_message(user_id, f"لديك جلسة جارية، تبقت {remaining//60} دقائق. إذا تريد إعادة البدء اضغط 'إنهاء درس اليوم ⛔' ثم ابدأ مجددًا.")
                    return

        # start session
        db.start_lesson_session(user_id)
        # generate lesson via AI
        level = u.get('level','A1')
        unit = u.get('unit',1)
        lesson = ai.generate_lesson(level, unit)
        text = f"📚 درس: مستوى {level} - وحدة {unit}\n\n{lesson.get('raw','لا يوجد محتوى')}\n\n✅ بعد إكمال الدرس تحصل على 1 coin."
        bot.send_message(user_id, text)
        # award coin for starting a lesson? reward defined as after finishing - we award at end or when user finishes.
        # We'll mark lesson completed immediately for simplicity (user can be stricter later)
        db.add_coins(user_id, COIN_REWARD)
        bot.send_message(user_id, f"تم منحك {COIN_REWARD} coin على إكمال الدرس. رصيدك الآن: {db.get_user(user_id)['coins']}")

    @bot.message_handler(func=lambda m: m.text == "إنهاء درس اليوم ⛔")
    def end_lesson(m: Message):
        user_id = m.chat.id
        u = db.get_user(user_id)
        if not u:
            bot.send_message(user_id, "سجّل أولاً باستخدام /start")
            return
        db.end_lesson_session(user_id)
        bot.send_message(user_id, "تم إنهاء جلسة الدرس لهذا اليوم. أراك غداً!", reply_markup=keyboards.main_menu())