import telebot
import openai
import pytesseract
from PIL import Image
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")

openai.api_key = OPENAI_KEY

bot = telebot.TeleBot(BOT_TOKEN)

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

Solve this question step by step.

Question:
{question}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return subject, response.choices[0].message.content


@bot.message_handler(commands=['start'])
def start(msg):

    bot.reply_to(msg,
"""
📚 Ultra AI Doubt Solver

Send your question:

Supported Subjects
• Physics
• Chemistry
• Maths
• Biology

You can send text or image.
""")


@bot.message_handler(content_types=['text'])
def text_solver(msg):

    question = msg.text

    subject, answer = ai_solver(question)

    bot.reply_to(msg,
f"""
📚 Subject: {subject}

✅ Solution:
{answer}
""")


@bot.message_handler(content_types=['photo'])
def image_solver(msg):

    file_info = bot.get_file(msg.photo[-1].file_id)
    downloaded = bot.download_file(file_info.file_path)

    with open("question.jpg","wb") as f:
        f.write(downloaded)

    img = Image.open("question.jpg")
    text = pytesseract.image_to_string(img)

    bot.reply_to(msg,"🔍 Question detected:\n"+text)

    subject, answer = ai_solver(text)

    bot.reply_to(msg,
f"""
📚 Subject: {subject}

✅ Solution:
{answer}
""")

bot.infinity_polling()
