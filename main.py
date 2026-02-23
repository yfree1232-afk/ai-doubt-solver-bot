import telebot
import os
from flask import Flask
import threading
import google.generativeai as genai

# ENV variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Telegram bot
bot = telebot.TeleBot(BOT_TOKEN)

# Gemini setup
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "🤖 AI DOUBT SOLVER BOT\n\n"
        "Send any Physics / Chemistry / Maths / Biology question.\n"
        "I will give step-by-step solution."
    )

# Question handler
@bot.message_handler(func=lambda message: True)
def solve_question(message):
    question = message.text

    try:
        response = model.generate_content(
            f"Solve this question with detailed step-by-step explanation:\n{question}"
        )

        answer = response.text

        bot.reply_to(message, answer)

    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")


# -------- Render keep alive server --------

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Doubt Solver Bot Running"


def run_bot():
    bot.infinity_polling()


threading.Thread(target=run_bot).start()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
