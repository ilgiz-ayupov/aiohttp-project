from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


def generate_quiz_start_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Начать викторину")]
    ], resize_keyboard=True)
    return keyboard
