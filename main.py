from flask import Flask
from threading import Thread
import telebot
from telebot import types

BOT_TOKEN = '8924802696:AAF92J5AfWghmLzz3_F6wRkYT96Th4ZFm9I'
AFFILIATE_LINK = 'https://baji1136.com/af/MrNBc5hM/Shamim'

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running 24/7!"

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🔥 এখনই একাউন্ট খুলুন 🔥", url=AFFILIATE_LINK)
    btn2 = types.InlineKeyboardButton("🎁 300% বোনাস নিন", callback_data="bonus")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, f"Welcome {message.from_user.first_name}!\n\n100% বোনাস পেতে নিচে ক্লিক করুন 👇", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    bot.send_message(call.message.chat.id, f"বোনাস লিংক:\n{AFFILIATE_LINK}")

def run():
    app.run(host='0.0.0.0',port=8080)

Thread(target=run).start()
bot.infinity_polling()
