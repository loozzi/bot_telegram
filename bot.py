import asyncio

from app import bot

print("Bot is running...")
asyncio.run(bot.polling())
