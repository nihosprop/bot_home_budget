import logging
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from filters.filters import IsNumber
from lexicon.lexicon_ru import LexiconCommandsRu, LexiconRu
from aiogram.types import (CallbackQuery,
                           Message,
                           BotCommand,
                           InlineKeyboardButton,
                           InlineKeyboardMarkup)


logger = logging.getLogger(__name__)
user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(LexiconRu.start)

@user_router.message(F.text.lower() == '/help')
async def cmd_help(message: Message):
    await message.answer(LexiconRu.help)
