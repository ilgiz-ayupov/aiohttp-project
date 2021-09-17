import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from .settings import BOT_TOKEN, WEBHOOK_URL

import requests

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler()
async def start(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, message.text)


def start_webhook():
    print(f"WEBHOOK установлен {WEBHOOK_URL}")
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}"
    response = requests.post(url)
    print(response.json())
    return response.status_code
