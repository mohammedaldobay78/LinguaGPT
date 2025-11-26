# lesson_ai.py

import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")


def get_lesson(level, unit):
    prompt = f"""
    Create an English lesson for:
    Level: {level}
    Unit: {unit}

    The lesson must include:
    - Title
    - 6 simple explanation bullet points
    - Examples included inside explanations

    Return response in this JSON format:
    {{
        "title": "...",
        "content": ["...", "..."]
    }}
    """

    response = model.generate_content(prompt)
    data = eval(response.text)

    return data["title"], data["content"]


def get_quiz(level, unit):
    prompt = f"""
    Create a quiz for:
    Level: {level}
    Unit: {unit}

    Make exactly 5 questions.
    Each question must have 4 choices.

    Return response in this JSON format:
    [
        {{
            "question": "...",
            "choices": ["A", "B", "C", "D"],
            "answer": 1
        }}
    ]
    """

    response = model.generate_content(prompt)
    questions = eval(response.text)

    return questions