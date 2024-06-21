from telebot import TeleBot

from app.config import Config

envConfig = Config()

bot = TeleBot(envConfig.TOKEN)

from app.BotController import BotController

botController = BotController(bot)


@bot.message_handler(commands=["start"])
def start(message):
    botController.start(message)


@bot.message_handler(commands=["help"])
def help(message):
    botController.help(message)


@bot.message_handler(func=lambda message: True)
def downloader(message):
    botController.downloader(message)
