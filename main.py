ADMIN_ID = 8251016419  
PAYOUT_CHANNEL = -1004369617531

bot = telebot.TeleBot(9147047095:AAFUXWKkXe29jDdOekLnggJL9ZFhK5tRqbA)
conn = sqlite3.connect('bot.db', check_same_thread=False)
conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, balance INTEGER DEFAULT 0)")
conn.commit()

@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id
    uname = f"@{m.from_user.username}" if m.from_user.username else m.from_user.first_name
    conn.execute("INSERT OR IGNORE INTO users (id, username, balance) VALUES (?,?,0)", (uid, uname))
    conn.commit()
    bot.send_message(m.chat.id, f"👋 Welcome {uname}!\n\nতোমার Username সেভ হয়েছে: {uname}\n\n💰 Balance: /balance\n💸 Withdraw: /withdraw")

@bot.message_handler(commands=['balance'])
def balance(m):
    cur = conn.execute("SELECT balance FROM users WHERE id=?", (m.from_user.id,)).fetchone()
    bot.send_message(m.chat.id, f"💰 Balance: ₹{cur[0] if cur else 0}")

@bot.message_handler(commands=['withdraw'])
def withdraw(m):
    msg = bot.send_message(m.chat.id, "💸 Amount লিখো (Min 10):")
    bot.register_next_step_handler(msg, do_withdraw)

def do_withdraw(m):
    try:
        amount = int(m.text)
        uid = m.from_user.id
        uname = f"@{m.from_user.username}" if m.from_user.username else m.from_user.first_name
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f"✅ Approve {amount}", callback_data=f"app_{uid}_{amount}_{uname}"),
                   types.InlineKeyboardButton("❌ Reject", callback_data=f"rej_{uid}"))
        
        text = f"💰 New Withdraw\n\n👤 User: {m.from_user.first_name}\n🆔 ID: {uid}\n👤 Username: {uname}\n💵 Amount: ₹{amount}"
        bot.send_message(ADMIN_ID, text, reply_markup=markup)
        bot.send_message(m.chat.id, f"✅ Request গেছে Admin এর কাছে\nUsername হিসেবে যাবে: {uname}")
    except:
        bot.send_message(m.chat.id, "সঠিক সংখ্যা দাও")

@bot.callback_query_handler(func=lambda x: True)
def callback(call):
    data = call.data.split("_")
    if data[0] == "app":
        uid = data[1]
        amount = data[2]
        uname = data[3]
      
        final = f"✅ Payment Done Successfully\n\n👤 Sent To (Username) :\n{uname}\n\n💰 Amount : ₹{amount}\n\nJoin @ridoy_caption_box_1"
        bot.send_message(PAYOUT_CHANNEL, final)
        bot.send_message(int(uid), f"✅ তোমার ₹{amount} Approve হয়েছে! Username: {uname}")
        bot.answer_callback_query(call.id, "Approved!")
    else:
        bot.send_message(int(data[1]), "❌ তোমার Withdraw Reject হয়েছে")
        bot.answer_callback_query(call.id, "Rejected!")

bot.polling()
