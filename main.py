import os
import re
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# --- 24 ঘন্টা চালু রাখার জন্য ---
app_flask = Flask(__name__)
app = app_flask # Render এর জন্য app নাম লাগবে
@app_flask.route('/')
def home():
    return "Baji Bot is Live 24/7!"

def run_flask():
    app_flask.run(host='0.0.0.0', port=10000)

# --- API Keys ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def get_number(text):
    mapping = {'১':1,'২':2,'৩':3,'৪':4,'৫':5,'এক':1,'দুই':2,'দুটো':2,'দুটা':2,'তিন':3,'তিনটা':3,'চার':4,'চারটা':4,'পাঁচ':5,'পাঁচটা':5,'1':1,'2':2,'3':3,'4':4,'5':5}
    for k,v in mapping.items():
        if k in text.lower():
            return v
    nums = re.findall(r'\d+', text)
    if nums:
        n = int(nums[0])
        return min(n, 5)
    return 1

def get_sport_type(text):
    text = text.lower()
    if 'ক্রিকেট' in text or 'cricket' in text:
        return 'cricket'
    if 'ফুটবল' in text or 'football' in text:
        return 'football'
    return 'all sports'

async def get_sports_news(count, sport_type):
    prompt = f"তুমি একজন খেলার খবর রিপোর্টার। আমাকে {sport_type} এর {count} টি সর্বশেষ খবর দাও। প্রতিটি খবর ছোট করে ২ লাইনে দাও, সাথে ইমোজি ব্যবহার করো। ভাষা: বাংলা। আজকের তারিখ ধরে খবর দাও।"
    try:
        completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
messages=[...
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"খবর আনতে সমস্যা হচ্ছে ভাই: {e}"

# 1 সেকেন্ডে গোল চেক
async def goal_1sec(context: ContextTypes.DEFAULT_TYPE):
    print("Checking goal - 1 sec")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    count = get_number(user_text)
    sport = get_sport_type(user_text)
    await update.message.reply_text(f"ঠিক আছে ভাই, {sport} এর {count} টা খবর আনছি... ⏳")
    news = await get_sports_news(count, sport)
    await update.message.reply_text(news)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "আসসালামু আলাইকুম ভাই! আমি রেডি ২৪/৭ 🔥\n\n"
        "এভাবে বলো:\n"
        "👉 '১টা খবর দাও'\n"
        "👉 '৩টা খেলার খবর দাও'\n"
        "👉 '৫টা ক্রিকেটের খবর দাও'\n"
        "👉 'ফুটবলের খবর দাও'\n"
        "তুমি যা বলবে আমি তাই দেবো!"
    )

# --- বট সেটআপ ---
application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
application.job_queue.run_repeating(goal_1sec, interval=1, first=1)

def run_bot():
    print("Bot is running 24/7... 1 sec check ON")
    application.run_polling()

# Render Gunicorn এর জন্য বট ব্যাকগ্রাউন্ডে চালু হবে
if BOT_TOKEN:
    threading.Thread(target=run_bot, daemon=True).start()

def main():
    threading.Thread(target=run_flask, daemon=True).start()
    run_bot()

if __name__ == '__main__':
    main()
