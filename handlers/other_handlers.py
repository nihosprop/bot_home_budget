import logging

from states.states import FSMMakeTransaction
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram import Router
from lexicon.lexicon_ru import LexiconRu


logger = logging.getLogger(__name__)
other_router = Router()

@other_router.message(StateFilter(FSMMakeTransaction.fill_number))
async def warning_not_number(message: Message):
    await message.answer(f'{LexiconRu.other_message}')
