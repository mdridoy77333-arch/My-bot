import telebot
import os
from flask import Flask
import threading

TOKEN = "9147047095:AAFUXWKKXe29jDdOekLnggJL9ZFhK5tRqbA"
bot = telebot.TeleBot(TOKEN)

# তোমার পুরনো সব @bot.message_handler কোড এখানে থাকবে
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot is Live! ✅")

# Flask app যাতে Render পোর্ট পায়
app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is Running!"

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

















    



