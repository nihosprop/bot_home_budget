import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram import F, Router

from lexicon.lexicon_ru import LexiconRu

logger_other_hand = logging.getLogger(__name__)
other_router = Router()


@other_router.message()
async def other_message(msg: Message, state: FSMContext):
    logger_other_hand.debug(f'Entry{await state.get_state()=}')
    await msg.answer(LexiconRu.text_problems)
    logger_other_hand.debug('Exit')


# cap
@other_router.callback_query()
async def other_clbk(clbk: CallbackQuery):
    await clbk.message.delete()
    await clbk.answer('Запустите бота\n'
                      'Меню -> /start', show_alert=True)
    await clbk.answer()
