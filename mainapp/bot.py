import logging

from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from .settings import BOT_TOKEN, WEBHOOK_URL
from . import keyboards, database

import requests

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    await bot.send_message(chat_id, text=f"Привет {first_name}")
    await register_user(message)
    await bot.send_message(chat_id, "Начать викторину ?", reply_markup=keyboards.generate_quiz_start_menu())


async def register_user(message: types.Message):
    """Регистрация пользователей в БД FireStore"""
    telegram_id = message.chat.id
    user_name = message.chat.username
    first_name = message.chat.first_name
    last_name = message.chat.last_name

    doc_ref = database.db.collection(u'users').document(str(telegram_id))
    doc_ref.set({
        u'userName': user_name,
        u'firstName': first_name,
        u'lastName': last_name,
        u'telegramId': telegram_id
    })
    await bot.send_message(telegram_id, "Авторизация прошла успешно !")


@dp.message_handler(lambda message: "Начать викторину" in message.text)
async def start_quiz(message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, "Викторина началась !")
    await send_question(message)


async def send_question(message: types.Message, question_id: int = 1):
    """Отправить пользователю вопрос"""
    chat_id = message.chat.id
    question_ref = database.db.collection(u'questions').document(str(question_id))
    question_doc = question_ref.get()

    print("ВОПРОС №", question_id)
    user_ref = database.db.collection(u'users').document(str(chat_id))
    user_doc = user_ref.get()

    if question_doc.exists and user_doc.exists:
        data = question_doc.to_dict()
        text = f"""<strong>Вопрос № {question_id}</strong>\n{data["question"]}"""
        await bot.send_message(chat_id, text, parse_mode="HTML",
                               reply_markup=keyboards.generate_answer_options_menu(data["answer_options"]))

        user_data = user_doc.to_dict()
        user_data["currentQuestion"] = user_data.get("currentQuestion", question_id) + 1
        user_ref.set(user_data)
    else:
        await bot.send_message(chat_id, "Вопрос не найден !")


@dp.message_handler(lambda message: True)
async def check_answer(message):
    chat_id = message.chat.id
    user_answer = message.text

    user = database.db.collection(u'users').document(str(chat_id))
    user_doc = user.get()
    user_data = user_doc.to_dict()

    question_id = user_data["currentQuestion"]
    question = database.db.collection(u'questions').document(str(question_id))
    question_doc = question.get()

    if question_doc.exists and user_doc.exists:
        question_data = question_doc.to_dict()
        await bot.send_message(chat_id, f"{user_answer} {question_data['answer']}")
        if question_data["answer"] == user_answer:
            user_data["true_answer"] = user_data.get("true_answer", 0) + 1
        else:
            user_data["false_answer"] = user_data.get("false_answer", 0) + 1
        user.set(user_data)
        await send_question(message, question_id)
    else:
        await bot.send_message(chat_id, "Вопрос не найден !")


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
