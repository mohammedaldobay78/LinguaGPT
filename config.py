# config.py
# ضع هنا التوكن والمفتاح كما طلبت
TELEGRAM_BOT_TOKEN = "8408899631:AAFT_FQzTqzgTZQE6BsdTGrXYUZa7mSZ004"
GEMINI_API_KEY = "AIzaSyDmJxFxuxEcWDKAWyn8Z2ndqrdiB_ZuFcI"

# اسم البوت
BOT_NAME = "LinguaGPT"

# المستويات المدعومة
LEVELS = ["A1", "A2", "B1", "B2", "C1"]

# مدة درس يومي بالثواني (1 ساعة)
DAILY_LESSON_SECONDS = 60 * 60

# عدد coins عند إنجاز درس/كويز
COIN_REWARD = 1

# أسعار الـ shop items (بـ coins)
SHOP_ITEMS = {
    "upgrade_a": 5,
    "upgrade_b": 5,
    "boost_quizzes": 8,
    "pronunciation_ai": 25,
    "learning_24h": 50,
    "daily_gift": 0  # daily gift handled separately
}

# أسماء عرض للعناصر
SHOP_NAMES = {
    "upgrade_a": "رفع مستوى الدروس A (5 coins)",
    "upgrade_b": "رفع مستوى الدروس B (5 coins)",
    "boost_quizzes": "رفع مستوى الكويزات (8 coins)",
    "pronunciation_ai": "فتح تصحيح النطق بالـ AI (25 coins)",
    "learning_24h": "ميزة التعلم 24 ساعة (50 coins)",
    "daily_gift": "الهدية اليومية (5 coins)"
}