from telebot.async_telebot import AsyncTeleBot

from app.BotController import BotController
from app.config import Config

envConfig = Config()

bot = AsyncTeleBot(envConfig.TOKEN)
hashed_table = {}


botController = BotController(bot, hashed_table)


@bot.message_handler(commands=["start"])
async def start(message):
    await botController.start(message)


@bot.message_handler(commands=["help"])
async def help(message):
    await botController.help(message)


@bot.message_handler(func=lambda message: True)
async def downloader(message):
    await botController.downloader(message)


@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    if call.data.startswith("Download"):
        await bot.answer_callback_query(call.id, "Đang tải xuống...")
        chat_id, message_id, encoded_data, _ = call.data.split("|")[1:]
        url = hashed_table[encoded_data]
        if "MP3" in call.data:
            await botController.handle_download_audio(chat_id, message_id, url)
        else:
            await botController.handle_download_video(chat_id, message_id, url)
    elif call.data.startswith("Cancel"):
        chat_id, message_id = call.data.split("|")[1:]
        await bot.delete_message(chat_id, message_id)
        await bot.answer_callback_query(call.id, "Đã hủy tải xuống")
