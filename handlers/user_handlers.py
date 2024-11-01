import logging
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from lexicon.lexicon_ru import LexiconCommandsRu, LexiconRu
from aiogram.types import CallbackQuery, Message, BotCommand


logger = logging.getLogger(__name__)
user_router = Router()
lexicon_ru = LexiconRu()

@user_router.message(CommandStart())
async def cmd_start(message: Message):
    pass


@user_router.message(F.text.lower() == '/help')
async def cmd_help(message: Message):
    await message.answer(lexicon_ru.help)
