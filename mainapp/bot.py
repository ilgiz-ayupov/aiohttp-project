import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook
from .settings import (BOT_TOKEN, WEBHOOK_URL, WEBHOOK_HOST,
                       WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT)

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware)


@dp.message_handler()
async def start(message: types.Message):
    chat_id = message.chat.id
    return SendMessage(chat_id, message.text)


async def on_startup(dp: Dispatcher):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp: Dispatcher):
    logging.warning("Выключение ...")

    await bot.delete_webhook()

    # Закрытие БД

    logging.warning("Пока !")


def start_bot():
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBHOOK_HOST,
        port=WEBAPP_PORT
    )
