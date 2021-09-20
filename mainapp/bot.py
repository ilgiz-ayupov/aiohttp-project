import logging
from datetime import datetime
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
    text = f"""Привет {first_name}!
Вас приветствует Бот-Викторина
Правила бота простые:
1. Бот авторизует вас. Для этого бот автоматически соберёт следующее данные:
    Имя
    Фамилию
    Имя пользователя
    Телеграм ID
    
2. Викторина начнётся, когда игрок нажмёт на кнопку "Начать викторину"
3. На каждый вопрос будет дано по 4 варианта ответа, в качестве кнопок
4. Вопрос не ограничен по времени
4. Нажимайте на кнопки, что бы ответить на вопрос. Иначе вам засчитается неверный ответ !
5. Выигрывает тот игрок который ответит правильно больше остальных игроков.
"""
    await bot.send_message(chat_id, text=text)
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

    user_ref = database.db.collection(u'users').document(str(chat_id))
    user_data = user_ref.get().to_dict()
    user_data["time_start"] = user_data.get("time_start", datetime.now())

    user_ref.set(user_data)
    await send_question(message)


async def send_question(message: types.Message, question_id: int = 1):
    """Отправить пользователю вопрос"""
    chat_id = message.chat.id
    question_ref = database.db.collection(u'questions').document(str(question_id))
    question_doc = question_ref.get()

    user_ref = database.db.collection(u'users').document(str(chat_id))
    user_doc = user_ref.get()
    user_data = user_doc.to_dict()

    if question_doc.exists and user_doc.exists:
        data = question_doc.to_dict()
        text = f"""<strong>Вопрос № {question_id}</strong>\n{data["question"]}"""
        await bot.send_message(chat_id, text, parse_mode="HTML",
                               reply_markup=keyboards.generate_answer_options_menu(data["answer_options"]))

        user_data["currentQuestion"] = user_data.get("currentQuestion", question_id) + 1
        user_ref.set(user_data)
    else:
        end_time = datetime.now()

        duration = end_time - user_data["time_start"]
        days, seconds = duration.days, duration.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        text = f"""Викторина закончилась !
Правильных ответов: {user_data["true_answer"]}
Неправильных ответов: {user_data["false_answer"]}
Время: {hours} часов {minutes} минут {seconds} секунд"""
        await bot.send_message(chat_id, "Вопрос не найден !")


@dp.message_handler()
async def check_answer(message):
    chat_id = message.chat.id
    user_answer = message.text

    user = database.db.collection(u'users').document(str(chat_id))
    user_doc = user.get()
    user_data = user_doc.to_dict()

    question_id = user_data["currentQuestion"] - 1
    question = database.db.collection(u'questions').document(str(question_id))
    question_doc = question.get()

    question_data = question_doc.to_dict()

    if question_doc.exists and user_doc.exists:
        if question_data["answer"] == user_answer:
            user_data["true_answer"] = user_data.get("true_answer", 0) + 1
        else:
            user_data["false_answer"] = user_data.get("false_answer", 0) + 1
        user.set(user_data)
        await send_question(message, user_data["currentQuestion"])
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
