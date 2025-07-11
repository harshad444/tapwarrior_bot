
import telebot
import sqlite3

API_TOKEN = 'YOUR_BOT_TOKEN_HERE'
bot = telebot.TeleBot(API_TOKEN)
conn = sqlite3.connect('tapwarrior.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, coins INTEGER DEFAULT 0, level INTEGER DEFAULT 1)")
conn.commit()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    cursor.execute("INSERT OR IGNORE INTO users (id) VALUES (?)", (user_id,))
    conn.commit()
    bot.reply_to(message, "🎯 Welcome to Tap Warrior!
Type /tap to earn coins.")

@bot.message_handler(commands=['tap'])
def tap(message):
    user_id = message.from_user.id
    user = cursor.execute("SELECT coins, level FROM users WHERE id=?", (user_id,)).fetchone()
    if user:
        coins, level = user
        coins += level
        cursor.execute("UPDATE users SET coins=? WHERE id=?", (coins, user_id))
        conn.commit()
        bot.reply_to(message, f"💰 +{level} coin(s)! Total coins: {coins}")
    else:
        bot.reply_to(message, "Please type /start first.")

@bot.message_handler(commands=['balance'])
def balance(message):
    user_id = message.from_user.id
    result = cursor.execute("SELECT coins, level FROM users WHERE id=?", (user_id,)).fetchone()
    if result:
        coins, level = result
        bot.reply_to(message, f"🧾 Balance: {coins} coins | Level: {level}")
    else:
        bot.reply_to(message, "Please type /start first.")

@bot.message_handler(commands=['upgrade'])
def upgrade(message):
    user_id = message.from_user.id
    result = cursor.execute("SELECT level, coins FROM users WHERE id=?", (user_id,)).fetchone()
    if result:
        level, coins = result
        cost_table = {
            1: 1000, 2: 2000, 3: 5000, 4: 10000, 5: 25000, 6: 50000, 7: 70000, 8: 100000,
            9: 150000, 10: 200000, 11: 250000, 12: 300000, 13: 350000, 14: 400000,
            15: 500000, 16: 600000, 17: 700000, 18: 800000, 19: 900000, 20: 1000000,
            21: 1100000, 22: 1200000, 23: 1300000, 24: 1500000
        }
        if level >= 25:
            bot.reply_to(message, "🎉 You have reached the maximum level (25)!")
            return
        cost = cost_table.get(level, None)
        if cost is None:
            bot.reply_to(message, "⚠️ No upgrade cost found for your level.")
            return
        if coins >= cost:
            cursor.execute("UPDATE users SET level = level + 1, coins = coins - ? WHERE id=?", (cost, user_id))
            conn.commit()
            bot.reply_to(message, f"✅ Upgrade successful! New level: {level + 1}")
        else:
            bot.reply_to(message, f"❌ Not enough coins. Upgrade cost: {cost}")
    else:
        bot.reply_to(message, "Please type /start first.")

bot.polling()
