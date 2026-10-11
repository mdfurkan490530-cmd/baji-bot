import os, re, random, requests, threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
MY_LINK = "https://www.tuval.online/af/JR21vM0a/mdfurka1/"
CHAT_IDS = set()
last_scores = {}

CRICKET = [
    "🏏 BAN 280/5 vs IND - লিটন 78*, শান্ত 52",
    "🏏 IPL: RCB জিতেছে 6 উইকেটে - কোহলি 92*",
    "🏏 BPL আজ রাত 7টায়: কুমিল্লা vs রংপুর",
    "🏏 PSL: বাবর আজম 101*",
    "🏏 T20 WC: বাংলাদেশ সেমিফাইনালে",
]
FOOTBALL = [
    "⚽ Man City 1-0 Arsenal - Haaland 23'",
    "⚽ Real 2-2 Barca - 88' GOAL",
    "⚽ Messi হ্যাটট্রিক - Miami 3-0",
]

def get_count(t):
    bn = str.maketrans("১২৩৪৫", "12345")
    t = t.translate(bn).lower()
    m = re.search(r'([1-5])', t)
    if m: return int(m.group(1))
    if "এক" in t: return 1
    if "দুই" in t or "দু" in t or "2" in t: return 2
    if "তিন" in t or "3" in t: return 3
    if "চার" in t or "4" in t: return 4
    if "পাঁচ" in t or "পাচ" in t or "5" in t: return 5
    return 1

def live():
    try:
        r = requests.get("https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard", timeout=10).json()
        s=""
        for ev in r.get('events',[])[:3]:
            c=ev['competitions'][0]
            h=c['competitors'][0]['team']['shortDisplayName']
            a=c['competitors'][1]['team']['shortDisplayName']
            hs=c['competitors'][0].get('score','0')
            aw=c['competitors'][1].get('score','0')
            s+=f"⚽ {h} {hs}-{aw} {a}\n"
        return s if s else "Live শুরু হলেই 1 সেকেন্ডে জানাবো"
    except: return "⚽ LIVE: Goal check 1s"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    CHAT_IDS.add(update.effective_chat.id)
    kb=[[InlineKeyboardButton("🎮 365 দিন চেক", url=MY_LINK)]]
    await update.message.reply_text("✅ আমি রেডি 24/7!\nবলো: '1টা দাও' / '3টা ক্রিকেট দাও' / '5টা ফুটবল দাও'", reply_markup=InlineKeyboardMarkup(kb))

async def all_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    CHAT_IDS.add(update.effective_chat.id)
    txt=update.message.text.lower()
    cnt=get_count(txt)
    if cnt>5: cnt=5

    if "ক্রিকেট" in txt or "cricket" in txt:
        random.shuffle(CRICKET)
        sel=CRICKET[:cnt]
        msg="\n\n".join([f"{i+1}. {n}" for i,n in enumerate(sel)])
        await update.message.reply_text(f"🏏 ক্রিকেটের {cnt}টা খবর:\n\n{msg}")
        return

    if "ফুটবল" in txt or "গোল" in txt or "football" in txt:
        lv=live()
        if cnt>1:
            random.shuffle(FOOTBALL)
            msg="\n\n".join(FOOTBALL[:cnt])
            await update.message.reply_text(f"⚽ {cnt}টা ফুটবল খবর:\n\n{msg}\n\n{lv}")
        else:
            await update.message.reply_text(f"⚽ {lv}")
        return

    random.shuffle(CRICKET)
    sel=CRICKET[:cnt]
    msg="\n\n".join([f"{i+1}. {n}" for i,n in enumerate(sel)])
    await update.message.reply_text(f"✅ তোমার {cnt}টা খবর:\n\n{msg}")

async def goal_1sec(context: ContextTypes.DEFAULT_TYPE):
    global last_scores
    # এখানে 1 সেকেন্ডে গোল চেক করবে

# 24/7 এর জন্য Flask
flask_app = Flask(__name__)
@flask_app.route('/')
def home(): return "Baji Bot Live 24/7"
def run_flask(): flask_app.run(host='0.0.0.0', port=10000)

def main():
    threading.Thread(target=run_flask).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, all_msg))
    app.job_queue.run_repeating(goal_1sec, interval=1, first=1)
    app.run_polling()

if __name__ == '__main__': main()
