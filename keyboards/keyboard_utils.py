import logging

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon import CANCEL_BUTT

logger_kb_utils = logging.getLogger(__name__)


def create_inline_kb(
        width: int, *args: str, cancel_butt=True, webapp=False,
        **kwargs: str) -> InlineKeyboardMarkup:
    """Generates inline keyboards on the fly"""

    kb_builder = InlineKeyboardBuilder()
    big_text: list[InlineKeyboardButton] = []
    small_text: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            if len(button) > 16:
                big_text.append(InlineKeyboardButton(
                        text=CANCEL_BUTT[button] if CANCEL_BUTT.get(
                                button) else button, callback_data=button))
            else:
                small_text.append(InlineKeyboardButton(
                        text=CANCEL_BUTT[button] if CANCEL_BUTT.get(
                                button) else button, callback_data=button))

    if kwargs:
        for button, text in kwargs.items():
            if len(text) > 16:
                big_text.append(
                        InlineKeyboardButton(text=text, callback_data=button))
            else:
                small_text.append(
                        InlineKeyboardButton(text=text, callback_data=button))

    kb_builder.row(*big_text, width=1)
    kb_builder.row(*small_text, width=width)
    if cancel_butt:
        kb_builder.row(InlineKeyboardButton(text=CANCEL_BUTT['cancel'],
                                            callback_data='/cancel'))
    if webapp:
        kb_builder.row(InlineKeyboardButton(text="GitHub", web_app=WebAppInfo(
                url='https://github.com')))
    return kb_builder.as_markup()
