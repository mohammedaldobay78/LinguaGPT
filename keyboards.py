# keyboards.py
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📘 الدروس"))
    kb.add(KeyboardButton("📝 اختبار (Poll)"))
    kb.add(KeyboardButton("🤖 محادثة AI"))
    kb.add(KeyboardButton("🎙 تحسين النطق"))
    kb.add(KeyboardButton("🛒 المتجر"))
    kb.add(KeyboardButton("🎁 الهدية اليومية"))
    kb.add(KeyboardButton("📊 تقدمي"))
    return kb

def lesson_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("ابدأ درس اليوم ▶️"))
    kb.add(KeyboardButton("إنهاء درس اليوم ⛔"))
    kb.add(KeyboardButton("عودة ⤴️"))
    return kb

def quiz_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("ابدأ الاختبار الآن"))
    kb.add(KeyboardButton("عودة ⤴️"))
    return kb

def shop_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("شراء: رفع مستوى A (5)"))
    kb.add(KeyboardButton("شراء: رفع مستوى B (5)"))
    kb.add(KeyboardButton("شراء: رفع الكويزات (8)"))
    kb.add(KeyboardButton("شراء: فتح تصحيح النطق (25)"))
    kb.add(KeyboardButton("شراء: learning 24h (50)"))
    kb.add(KeyboardButton("عودة ⤴️"))
    return kb