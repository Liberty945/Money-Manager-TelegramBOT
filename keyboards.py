from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton('Остаток средств'),
        KeyboardButton('Список операций'),
    )

    return keyboard   #Функция создания клавиатуры


def get_inline_keyboard() -> InlineKeyboardMarkup:
    inl_keyboard = InlineKeyboardMarkup(row_width=2)
    inl_keyboard.add(
        InlineKeyboardButton('Добавить поступления', callback_data='kb_plus'),
        InlineKeyboardButton('Добавить расходы', callback_data='kb_minus'),
    )

    return inl_keyboard   #Функция создания инлайн клавиатуры