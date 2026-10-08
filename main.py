
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN")
MY_LINK = "https://www.tuval.online/af/JR2T0P5L/join"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    keyboard = [[InlineKeyboardButton("👉 একাউন্ট খুলুন 👈", url=MY_LINK)]]
    text = f"হ্যালো {name} ভাই! 👋\nআমি তোমার বাজি হেল্পার বট।\nযেকোনো প্রশ্ন করো, আমি উত্তর দিবো।"
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def reply_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower()
    
    if "একাউন্ট" in msg or "account" in msg or "খুলব" in msg:
        ans = "একাউন্ট খুলতে নিচের বাটনে ক্লিক করো। Join Now এ চাপ দিয়ে 2 মিনিটে খুলে যাবে।"
    elif "ডিপোজিট" in msg or "টাকা" in msg:
        ans = "ডিপোজিট করতে একাউন্টে Login করে Deposit > bKash/Nagad সিলেক্ট করে 500 টাকা থেকে শুরু করতে পারবে।"
    elif "বোনাস" in msg or "bonus" in msg:
        ans = "প্রথম ডিপোজিটে বোনাস পেতে অবশ্যই আমার লিংক থেকে একাউন্ট খুলতে হবে।"
    elif "উইথড্র" in msg or "তুলব" in msg:
        ans = "উইথড্র করতে Withdraw এ গিয়ে bKash/Nagad দাও, 5 মিনিটে টাকা পাবে।"
    else:
        ans = f"তুমি বলেছো: {update.message.text}\n\nএটা নিয়ে হেল্প লাগলে বলো, আমি সাথে সাথে হেল্প করবো।"

    keyboard = [[InlineKeyboardButton("🔗 আমার লিংক থেকে জয়েন করুন 🔗", url=MY_LINK)]]
    await update.message.reply_text(ans, reply_markup=InlineKeyboardMarkup(keyboard))

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_all))
app.run_polling()
