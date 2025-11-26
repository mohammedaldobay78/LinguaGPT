# pronunciation_ai.py

import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-pro")


def evaluate_pronunciation(original_text, transcript):
    prompt = f"""
    Compare the following two texts:

    Original:
    {original_text}

    Spoken (transcribed):
    {transcript}

    Evaluate pronunciation from (0–10).
    Give short feedback.

    Return JSON:
    {{
        "score": 0-10,
        "feedback": "..."
    }}
    """

    response = model.generate_content(prompt)
    data = eval(response.text)

    return data["score"], data["feedback"]