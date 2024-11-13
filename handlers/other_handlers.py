import logging

from aiogram.types import Message, CallbackQuery
from aiogram import Router
from lexicon.lexicon_ru import LexiconRu


other_hand_logger = logging.getLogger(__name__)
other_router = Router()

@other_router.message()
async def other_message(msg: Message):
    await msg.answer(LexiconRu.problems)

# cap
@other_router.callback_query()
async def other_clbk(clbk: CallbackQuery):
    await clbk.message.delete()
    await clbk.message.answer('Запустите бота -> /start')
