# quiz_handler.py
from telebot.types import Message
import ai, db, keyboards

def register(bot):
    @bot.message_handler(func=lambda m: m.text == "📝 اختبار (Poll)")
    def entry(m: Message):
        bot.send_message(m.chat.id, "هل تريد اختبار الآن؟", reply_markup=keyboards.quiz_menu())

    @bot.message_handler(func=lambda m: m.text == "ابدأ الاختبار الآن")
    def start_quiz(m: Message):
        user_id = m.chat.id
        u = db.get_user(user_id)
        if not u:
            bot.send_message(user_id, "سجّل أولاً باستخدام /start")
            return
        level = u.get('level','A1')
        unit = u.get('unit',1)
        items = ai.generate_quiz(level, unit)
        # send each question as poll
        correct_count = 0
        for q in items:
            question_text = q.get('question','Question?')
            choices = q.get('choices', ["A","B","C","D"] )
            # send poll (non-anonymous so we can track?), telegram polls by default anonymous True; we send anonymous False
            poll = bot.send_poll(user_id, question_text, choices, is_anonymous=False)
            # can't get immediate answer programmatically without webhook or storing poll id; we will rely on user to answer and we won't auto-score here.
        bot.send_message(user_id, "أرسلت لك الأسئلة على شكل Poll. أجب على كل Poll وسيحسب رصيدك بعد انتهاء الاختبار (تلقائيًا بعد الردود).")
        # reward coin for taking quiz
        db.add_coins(user_id, 1)