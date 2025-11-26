# ai.py
from google import genai
import os
from config import GEMINI_API_KEY

# configure gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

def ask_gemini(prompt: str, max_output_chars: int = 1500) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text or ""
    except Exception as e:
        return f"⚠️ خطأ في الاتصال بالـ AI: {e}"

# helper: create lesson on the fly
def generate_lesson(level: str, unit: int) -> dict:
    prompt = f"""
You are an English teacher. Create a concise lesson for level {level}, unit {unit}.
Requirements:
- Lesson duration ~ 1 hour of active activities.
- Provide a lesson title.
- Provide 6 short bullet points explaining the grammar/vocab.
- Provide 5 short practice activities (one-line each).
Return as plain text sections separated by '---' like:
Title: ...
Bullets:
- ...
Exercises:
1) ...
"""
    text = ask_gemini(prompt)
    # return raw text; handler will format for Telegram
    return {"raw": text}

# helper: generate quiz (Telegram Poll)
def generate_quiz(level: str, unit: int) -> list:
    prompt = f"""
Generate exactly 4 multiple-choice questions for level {level} unit {unit}.
Each question must have 4 choices and indicate the correct choice number on the same line at the end like: (answer: 2)
Return as plain text, questions separated by blank lines.
"""
    text = ask_gemini(prompt)
    # parse into list of dicts
    items = []
    try:
        parts = [p.strip() for p in text.split("\n\n") if p.strip()]
        for p in parts:
            lines = [l.strip() for l in p.split("\n") if l.strip()]
            if not lines: continue
            q_line = lines[0]
            choices = []
            answer = 1
            for ln in lines[1:]:
                if ln.lower().startswith(("a)","1)","a.","1.")):
                    choices.append(ln.split(")",1)[1].strip() if ")" in ln else ln)
                else:
                    choices.append(ln)
                if 'answer:' in ln.lower():
                    try:
                        answer = int(ln.lower().split('answer:')[-1].strip())
                    except:
                        pass
            items.append({"question": q_line, "choices": choices[:4], "answer": answer})
    except Exception:
        pass
    # fallback: if parse failed, produce simple placeholders
    if not items:
        for i in range(4):
            items.append({"question": f"Sample question {i+1}", "choices": ["A","B","C","D"], "answer": 1})
    return items

# transcription: try using Gemini (if supported) else fallback to SpeechRecognition
def transcribe_audio(filepath: str) -> str:
    try:
        # attempt Gemini-style transcription via content API if audio supported
        # official approach may vary; we try a simple prompt + base64 content — if fails, fallback
        with open(filepath, "rb") as f:
            data = f.read()
        prompt = "Transcribe the following audio (English). If noise, give best guess.\n\n<MEDIA_BYTES>"
        # some Gemini SDKs accept a list items; this is a best-effort attempt:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt, data]
            )
            if response and response.text:
                return response.text
        except Exception:
            pass
    except Exception:
        pass

    # fallback using SpeechRecognition
    try:
        import speech_recognition as sr
        from pydub import AudioSegment
        # convert ogg/oggopus to wav if needed
        wav_path = filepath + ".wav"
        sound = AudioSegment.from_file(filepath)
        sound.export(wav_path, format="wav")
        r = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio = r.record(source)
        text = r.recognize_google(audio, language="en-US")
        return text
    except Exception as e:
        return f"[لا يمكن تحويل الصوت إلى نص: {e}]"