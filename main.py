import os, re, threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

app_flask = Flask(__name__)
app = app_flask

@app_flask.route('/')
def home():
    return "Baji Bot Live - OK"

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

def get_number(t):
    m={'১':1,'২':2,'৩':3,'৪':4,'৫':5,'এক':1,'দুই':2,'তিন':3,'চার':4,'পাঁচ':5,'1':1,'2':2,'3':3,'4':4,'5':5}
    for k,v in m.items():
        if k in t.lower(): return v
    n=re.findall(r'\d+',t)
    return min(int(n[0]),5) if n else 1

def get_sport_type(t):
    t=t.lower()
    if 'ক্রিকেট' in t: return 'cricket'
    if 'ফুটবল' in t: return 'football'
    return 'all sports'

async def get_news(c,s):
    p=f"আমাকে {s} এর {c} টি খবর দাও, ২ লাইনে, বাংলায়"
    try:
        r=client.chat.completions.create(model="llama-3.1-8b-instant",messages=[{"role":"user","content":p}])
        return r.choices[0].message.content
    except Exception as e: return f"Error: {e}"

async def handle(update, context):
    txt=update.message.text
    cnt=get_number(txt); sp=get_sport_type(txt)
    await update.message.reply_text(f"{sp} এর {cnt} টা খবর আনছি... ⏳")
    nw=await get_news(cnt,sp)
    await update.message.reply_text(nw)

async def start(update, context):
    await update.message.reply_text("রেডি ভাই 🔥 '৩টা খবর দাও' লিখো")

application = Application.builder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start",start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,handle))

def run_bot():
    application.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot,daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app_flask.run(host="0.0.0.0", port=port)
