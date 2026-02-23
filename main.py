import telebot
import google.generativeai as genai
import os
from flask import Flask
from threading import Thread

# ====== CONFIG ======
BOT_TOKEN = "YOUR_BOT_TOKEN"
GEMINI_API = "YOUR_GEMINI_API"

bot = telebot.TeleBot(BOT_TOKEN)

genai.configure(api_key=GEMINI_API)
model = genai.GenerativeModel("gemini-pro")

# ====== TELEGRAM BOT ======

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🤖 Send me any question, I will solve it using AI.")

@bot.message_handler(func=lambda m: True)
def solve(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")

# ====== PORT SERVER (RENDER FIX) ======

app = Flask('')

@app.route('/')
def home():
    return "Bot Running ✅"

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ====== START ======

keep_alive()
bot.infinity_polling()
