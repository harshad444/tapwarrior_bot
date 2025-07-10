
import telebot
bot = telebot.TeleBot("7968402839:AAElc7pzA3PsSsmtr24b3wSmDMB1OzM-gVU")

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Welcome to Tap Warrior!")

bot.polling()
