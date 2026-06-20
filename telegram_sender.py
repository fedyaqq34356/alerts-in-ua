from aiogram import Bot
from aiogram.enums import ParseMode
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_message_to_channel(text: str):
    await bot.send_message(
        chat_id=TELEGRAM_CHANNEL_ID, 
        text=text,
        parse_mode=ParseMode.HTML
    )