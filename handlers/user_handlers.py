import logging
from aiogram import Router, F
from lexicon.lexicon_ru import LexiconCommandsRu
from aiogram.types import CallbackQuery, Message

logger = logging.getLogger(__name__)
user_router = Router()


@user_router.message(F.text.lower() == '/help')
async def cmd_help(message: Message):
    await message.answer('Это команда /help')
