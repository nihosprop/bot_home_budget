import logging

from aiogram.types import Message
from aiogram import Router
from lexicon.lexicon_ru import LexiconRu


logger = logging.getLogger(__name__)
other_router = Router()
lexicon = LexiconRu()

@other_router.message()
async def answer_to_another(message: Message):
    await message.answer(f'{lexicon.other_message}')
