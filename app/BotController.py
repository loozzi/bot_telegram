from telebot import TeleBot

from app.logger import logger


class BotController:
    def __init__(self, bot: TeleBot):
        self.bot = bot

    def start(self, message):
        reply_message = "Xin chào, tôi là bot tải nội dung từ Tiktok, Douyin, Youtube, Instagram...\nĐể sử dụng bot vui lòng gửi link đến video/hình ảnh muốn tải về nhé!"
        self.bot.reply_to(message, reply_message)
        logger.info(reply_message)

    def help(self, message):
        reply_message = (
            "Để sử dụng bot vui lòng gửi link đến video/hình ảnh muốn tải về nhé!"
        )
        self.bot.reply_to(message, reply_message)
        logger.info(reply_message)

    def downloader(self, message):
        pass
