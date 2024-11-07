import logging

from states.states import FSMMakeTransaction
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram import Router
from lexicon.lexicon_ru import LexiconRu


logger = logging.getLogger(__name__)
other_router = Router()

@other_router.message()
async def other_message(msg: Message):
    await msg.answer('Что-то пошло не так. Нажмите\n/start')
