# voice_handler.py
from telebot.types import Message
import os, tempfile
import ai, db

def register(bot):
    @bot.message_handler(func=lambda m: m.text == "🎙 تحسين النطق")
    def ask_for_voice(m: Message):
        bot.send_message(m.chat.id, "أرسل مقطع صوتي تقرأ فيه الجملة أو الفقرة التي تريد تقييم نطقك لها.")

    @bot.message_handler(content_types=['voice', 'audio'])
    def handle_voice(m: Message):
        user_id = m.chat.id
        u = db.get_user(user_id)
        if not u:
            bot.send_message(user_id, "سجل أولًا باستخدام /start")
            return
        # check if user bought pronunciation feature
        if not u.get('vip_pronunciation',0):
            bot.send_message(user_id, "يجب عليك شراء ميزة تصحيح النطق من المتجر أولاً.")
            return

        # download file to temp
        file_info = bot.get_file(m.voice.file_id if m.content_type=='voice' else m.audio.file_id)
        downloaded = bot.download_file(file_info.file_path)
        with tempfile.NamedTemporaryFile(suffix=".ogg", delete=True) as tmp:
            tmp.write(downloaded)
            tmp.flush()
            # transcribe
            transcript = ai.transcribe_audio(tmp.name)
        # analyze pronunciation using AI
        # user said audio; we transcribed to text then send to AI for evaluation
        eval_prompt = f"User Read: {transcript}\nEvaluate pronunciation out of 10 and give short feedback and list mispronounced words."
        eval_result = ai.ask_gemini(eval_prompt)
        # save in DB
        # Try to pick numeric score from eval_result; if fails, save full as feedback and score 0
        score = 0.0
        # naive parse: look for number
        import re
        mnum = re.search(r'(\d+(\.\d+)?)', eval_result)
        if mnum:
            score = float(mnum.group(1))
        db.save_pronunciation(user_id, transcript, score, eval_result)
        bot.send_message(user_id, f"🔊 نص التحويل:\n{transcript}\n\n📋 تقييم:\n{eval_result}")