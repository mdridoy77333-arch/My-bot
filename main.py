import telebot
from telebot import types
import sqlite3

BOT_TOKEN = "9147047095:AAFUXWKkXe29jDdOekLnggJL9ZFhK5tRqbA"
ADMIN_ID = 8251016419
PAYOUT_CHANNEL = -1004369617531

bot = telebot.TeleBot(BOT_TOKEN)
conn = sqlite3.connect('bot.db', check_same_thread=False)
conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, balance INTEGER DEFAULT 0)")
conn.commit()

@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id
    uname = f"@{m.from_user.username}" if m.from_user.username else m.from_user.first_name
    conn.execute("INSERT OR IGNORE INTO users (id, username, balance) VALUES (?,?,0)", (uid, uname))
    conn.commit()
    bot.send_message(m.chat.id, f"Welcome {uname}! Username saved: {uname}")

@bot.message_handler(commands=['withdraw'])
def withdraw(m):
    msg = bot.send_message(m.chat.id, "Amount লিখো:")
    bot.register_next_step_handler(msg, do_withdraw)

def do_withdraw(m):
    amount = m.text
    uid = m.from_user.id
    uname = f"@{m.from_user.username}" if m.from_user.username else m.from_user.first_name
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Approve", callback_data=f"app_{uid}_{amount}_{uname}"))
    bot.send_message(ADMIN_ID, f"Withdraw\nUser: {uname}\nAmount: {amount}", reply_markup=markup)
    bot.send_message(m.chat.id, f"Request sent as {uname}")

@bot.callback_query_handler(func=lambda x: True)
def cb(call):
    _, uid, amount, uname = call.data.split("_")
    final = f"✅ Payment Done\n\n👤 Sent To (Username) :\n{uname}\n\n💰 Amount : ₹{amount}"
    bot.send_message(PAYOUT_CHANNEL, final)
    bot.send_message(int(uid), f"Approved ₹{amount} to {uname}")

bot.polling()
