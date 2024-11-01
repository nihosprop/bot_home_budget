from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import CATEGORY_1

def create_inline_kb(
        width: int, *args: str, **kwargs: str) -> InlineKeyboardMarkup:
    """Generates inline keyboards on the fly"""

    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(text=CATEGORY_1[button] if
            CATEGORY_1.get(button) else button, callback_data=button))

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=button))

    kb_builder.row(*buttons, width=width)
    kb_builder.row(InlineKeyboardButton(text='Отмена', callback_data='last_btn'))
    return kb_builder.as_markup()
