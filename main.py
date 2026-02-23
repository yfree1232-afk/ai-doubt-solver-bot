import telebot
import os
from openai import OpenAI
import pytesseract
from PIL import Image
from flask import Flask
import threading
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot running"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = threading.Thread(target=run)
    t.start()

keep_alive()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_KEY)

def detect_subject(q):

    q = q.lower()

    if any(x in q for x in ["integrate","derivative","equation"]):
        return "Mathematics"

    if any(x in q for x in ["force","velocity","acceleration"]):
        return "Physics"

    if any(x in q for x in ["reaction","mole","compound"]):
        return "Chemistry"

    if any(x in q for x in ["cell","dna","photosynthesis"]):
        return "Biology"

    return "Science"


def ai_solver(question):

    subject = detect_subject(question)

    prompt = f"""
You are an expert teacher.

Subject: {subject}

Solve this question step by step and explain simply.

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return subject, response.choices[0].message.content


@bot.message_handler(commands=['start'])
def start(msg):

    bot.reply_to(msg,
"""📚 Ultra AI Doubt Solver

Send your question.

Subjects supported:
Physics
Chemistry
Maths
Biology
""")


@bot.message_handler(content_types=['text'])
def text_solver(msg):

    question = msg.text

    try:
        subject, answer = ai_solver(question)

        bot.reply_to(msg,
f"""📚 Subject: {subject}

✅ Solution:
{answer}
""")

    except Exception as e:
        bot.reply_to(msg,"⚠️ Error: " + str(e))


bot.infinity_polling()
