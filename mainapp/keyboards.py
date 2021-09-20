from aiogram.types.reply_keyboard import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def generate_quiz_start_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Начать викторину")]
    ], resize_keyboard=True)


def generate_answer_options_menu(answer_options: list, max_quantity: int = 2) -> ReplyKeyboardMarkup:
    start = 0
    end = max_quantity
    rows = len(answer_options) // max_quantity
    if len(answer_options) % max_quantity != 0:
        rows += 1

    buttons = []
    for i in range(rows):
        new_lst = []
        for option in answer_options[start:end]:
            new_lst.append(KeyboardButton(text=option))
        buttons.append(new_lst)
        start = end
        end += max_quantity
    return ReplyKeyboardMarkup(keyboard=buttons, row_width=2)


def generate_remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()