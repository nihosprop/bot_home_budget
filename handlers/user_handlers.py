import logging

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import (CallbackQuery, Message)

from filters.filters import IsNumber
from keyboards.keyboard_utils import create_inline_kb
from lexicon.lexicon_ru import LEXICON, LexiconRu

logger = logging.getLogger(__name__)
user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(LexiconRu.start)


@user_router.message(F.text.lower() == '/help')
async def cmd_help(message: Message):
    await message.answer(LexiconRu.help)


@user_router.message(IsNumber())
async def number_input(message: Message):
    keyboard = create_inline_kb(4, **LEXICON)
    await message.answer(LexiconRu.select_categories, reply_markup=keyboard)


@user_router.callback_query(F.data.in_(LEXICON))
async def process_button_press(callback: CallbackQuery):
    await callback.answer()
