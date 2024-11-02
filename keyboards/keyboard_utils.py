from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon_ru import BUTTONS

# to make universal 
def create_inline_kb(
        width: int, *args: str, **kwargs: str) -> InlineKeyboardMarkup:
    """Generates inline keyboards on the fly"""

    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(text=BUTTONS[button] if
            BUTTONS.get(button) else button, callback_data=button))

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=button))

    kb_builder.row(*buttons, width=width)
    kb_builder.row(InlineKeyboardButton(text=BUTTONS['cancel'],
                                        callback_data='/cancel'))
    return kb_builder.as_markup()
