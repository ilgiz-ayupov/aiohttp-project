from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


def generate_quiz_start_menu():
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Начать викторину")]
    ])
    return keyboard
