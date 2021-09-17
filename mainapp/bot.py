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
    delete_webhook = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?drop_pending_updates=True"
    requests.post(delete_webhook)

    print(f"WEBHOOK установлен {WEBHOOK_URL}")
    set_webhook = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    response = requests.post(set_webhook, params={
        "url": WEBHOOK_URL,
        "max_connections": 1,
        "drop_pending_updates": True
    })
    return response.status_code
