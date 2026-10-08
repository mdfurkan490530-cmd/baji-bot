
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN")
MY_LINK = "https://www.tuval.online/af/JR2T0P5L/join"
BOT_USERNAME = "YOUR_BOT_USERNAME" # এখানে @ ছাড়া তোমার বটের নাম দিবে যেমন baji_helper_bot

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    # ভাইরাল শেয়ার বাটন
    share_text = f"🔥 এই বটে একাউন্ট খুললে বোনাস পাওয়া যায়! {MY_LINK}"
    share_url = f"https://t.me/share/url?url={MY_LINK}&text={share_text}"
    
    keyboard = [
        [InlineKeyboardButton("👉 একাউন্ট খুলুন - বোনাস নিন", url=MY_LINK)],
        [InlineKeyboardButton("🚀 বন্ধুকে শেয়ার করুন", url=share_url)],
        [InlineKeyboardButton("💬 সাপোর্ট", url=MY_LINK)]
    ]
    text = f"হ্যালো {name} ভাই! 👋\n\nআমি Baji Helper Bot।\n✅ যেকোনো প্রশ্নের উত্তর দিবো\n✅ একাউন্ট, ডিপোজিট, বোনাস সব হেল্প করবো\n\nনিচের বাটনে ক্লিক করে শুরু করুন 👇"
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def reply_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    
    share_text = f"এই বটটা দেখো, অটো উত্তর দেয়! {MY_LINK}"
    share_url = f"https://t.me/share/url?url={MY_LINK}&text={share_text}"

    keyboard = [
        [InlineKeyboardButton("🔗 আমার লিংকে জয়েন করুন", url=MY_LINK)],
        [InlineKeyboardButton("📤 শেয়ার করে আয় করুন", url=share_url)]
    ]
    
