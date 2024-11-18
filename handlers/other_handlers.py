import logging

from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from lexicon.lexicon_ru import LexiconRu


logger_other_hand = logging.getLogger(__name__)
other_router = Router()

@other_router.message()
async def other_message(msg: Message):
    await msg.answer(LexiconRu.text_problems)

# cap
@other_router.callback_query(F.data != '/start')
async def other_clbk(clbk: CallbackQuery):
    await clbk.message.delete()
    await clbk.answer('Запустите бота\n'
                      'Меню -> /start', show_alert=True)
