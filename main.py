import telebot, os, threading
from flask import Flask

TOKEN = "9147047095:AAFUXWKkXe29jDdOekLnggJL9ZFhK5tRqbA"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Bot is Live! ✅ Finally Ready!")

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Running OK"

def run_bot():
    bot.delete_webhook()
    print("Bot polling started...")
    bot.infinity_polling()

threading.Thread(target=run_bot).start()
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

















    



