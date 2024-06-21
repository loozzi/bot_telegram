import hashlib

import requests
from telebot import TeleBot, types
from telebot.util import quick_markup

from app.logger import logger
from app.services.Douyin import DouyinDownloader
from app.services.FileService import FileService
from app.services.Tiktok import TiktokDownloader


class BotController:
    def __init__(self, bot: TeleBot, hashed_table: dict = {}):
        self.bot = bot
        self.tiktokDownloader = TiktokDownloader()
        self.douyinDownloader = DouyinDownloader()
        self.fileService = FileService()
        self.hashed_table = hashed_table

    async def start(self, message):
        reply_message = (
            "Xin chào, tôi là bot tải nội dung từ Tiktok, Douyin, Youtube, Instagram.."
            + "\nĐể sử dụng bot vui lòng gửi link đến video/hình ảnh muốn tải về nhé!"
        )
        await self.bot.reply_to(message, reply_message)
        logger.info(reply_message)

    async def help(self, message):
        reply_message = (
            "Để sử dụng bot vui lòng gửi link đến video/hình ảnh muốn tải về nhé!"
        )
        await self.bot.reply_to(message, reply_message)
        logger.info(reply_message)

    async def downloader(self, message):
        if "tiktok" in message.text:
            await self.show_options(message, self.tiktokDownloader)
        elif "douyin" in message.text:
            await self.show_options(message, self.douyinDownloader)

            # self.bot.send_message(message.chat.id, "Choose:", reply_markup=markup)

    async def show_options(self, message, service):
        msg = await self.bot.reply_to(message, "Searching...")
        data = service.extract_video(message.text.split(" ")[0])
        if data["status"] == "error":
            await self.bot.edit_message_text(
                chat_id=message.chat.id,
                text=data["message"],
                message_id=msg.message_id,
            )
        else:
            await self.bot.delete_message(
                chat_id=message.chat.id, message_id=msg.message_id
            )
            buttons = {}
            for button in data["buttons"]:
                original_data = button["url"]
                hashed_data = hashlib.sha256(original_data.encode()).hexdigest()[:10]
                buttons[f"{button['title']} ✅"] = {
                    "callback_data": f"Download|{message.chat.id}|{message.message_id}|{hashed_data}|{button['title']}"
                }
                self.hashed_table[hashed_data] = original_data

            markup = quick_markup(
                buttons,
                row_width=2,
            )
            try:
                image = await self.fileService.save(data["cover"], "image.jpg")
                msg = await self.bot.send_photo(
                    chat_id=message.chat.id,
                    photo=open(f"./files/{image}", "rb"),
                    caption=f"<b>{data['username']}</b> - {data['description']}",
                    reply_to_message_id=message.message_id,
                    reply_markup=markup,
                    parse_mode="HTML",
                )
                buttons["Cancel ❌"] = {
                    "callback_data": f"Cancel|{message.chat.id}|{msg.message_id}"
                }
                markup = quick_markup(
                    buttons,
                    row_width=2,
                )

                await self.bot.edit_message_reply_markup(
                    chat_id=message.chat.id,
                    message_id=msg.message_id,
                    reply_markup=markup,
                )
                self.fileService.delete(image)
            except Exception as e:
                logger.error(e)
                if len(data["photos"]) > 0:
                    # for photo in data["photos"]:

                    #     await self.bot.send_message(
                    #         chat_id=message.chat.id,
                    #         text=photo,
                    #         reply_to_message_id=message.message_id,
                    #         reply_markup=markup,
                    #     )

                    media = []

                    for photo in data["photos"]:
                        media.append(types.InputMediaPhoto(requests.get(photo).content))

                    await self.bot.send_media_group(
                        chat_id=message.chat.id,
                        media=media,
                        reply_to_message_id=message.message_id,
                        reply_markup=markup,
                    )

                else:
                    await self.bot.send_message(
                        chat_id=message.chat.id,
                        text="Không thể tải ảnh đại diện!",
                        reply_to_message_id=message.message_id,
                        reply_markup=markup,
                    )

    async def handle_download_video(self, chat_id: int, message_id: int, url: str):
        video = await self.fileService.save(url)

        await self.bot.send_video(
            chat_id=chat_id,
            video=open(f"./files/{video}", "rb"),
            caption="Video đã được tải về thành công!",
            parse_mode="HTML",
            reply_to_message_id=message_id,
        )

        self.fileService.delete(video)

    async def handle_download_audio(self, chat_id: int, message_id: int, url: str):
        audio = await self.fileService.save(url, "audio.mp3")

        await self.bot.send_audio(
            chat_id=chat_id,
            audio=open(f"./files/{audio}", "rb"),
            caption="Audio đã được tải về thành công!",
            parse_mode="HTML",
            reply_to_message_id=message_id,
        )

        self.fileService.delete(audio)
