import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from .settings import BOT_TOKEN, WEBHOOK_URL
from . import keyboards

import requests

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler()
async def start(message: types.Message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    await bot.send_message(chat_id, text=f"Привет {first_name}")

    await bot.send_message(chat_id, "Начать викторину ?", reply_markup=keyboards.generate_quiz_start_menu())


@dp.message_handler(lambda message: "Начать викторину" in message.text)
async def start_quiz(message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Викторина началась !")


def start_webhook():
    delete_webhook = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?drop_pending_updates=True"
    requests.post(delete_webhook)

    print(f"WEBHOOK установлен {WEBHOOK_URL}")
    set_webhook = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    response = requests.post(set_webhook, params={
        "url": WEBHOOK_URL,
        "max_connections": 40,
        "drop_pending_updates": True
    })
    return response.status_code
