from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton


def generate_quiz_start_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Начать викторину")]
    ], resize_keyboard=True)


def generate_answer_options_menu(answer_options: list) -> ReplyKeyboardMarkup:
    buttons = [KeyboardButton(text=option) for option in answer_options]
    return ReplyKeyboardMarkup(keyboard=[*buttons], row_width=2)
