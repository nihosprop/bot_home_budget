import logging
from turtledemo.penrose import start

from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import (CallbackQuery, Message)
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from filters.filters import IsNumber
from keyboards.keyboard_utils import create_inline_kb
from lexicon.lexicon_ru import DIRECTION, LexiconRu, GAIN_CATEGORIES
from states.states import FSMMakeTransaction


logger = logging.getLogger(__name__)
user_router = Router()

@user_router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(LexiconRu.start)
    await state.set_state(FSMMakeTransaction.fill_number)

@user_router.callback_query(F.data == '/cancel', ~StateFilter(default_state))
async def process_cancel_command_state(callback: CallbackQuery,
                                       state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(LexiconRu.waiting_number)
    await state.set_state(FSMMakeTransaction.fill_number)

@user_router.message(StateFilter(FSMMakeTransaction.fill_number), IsNumber())
async def process_number_sent(message: Message, state: FSMContext):
    keyboard = create_inline_kb(4, **DIRECTION)
    await state.update_data(amount=int(message.text))
    await message.answer(LexiconRu.select_direction, reply_markup=keyboard)
    await state.set_state(FSMMakeTransaction.select_direction)

@user_router.callback_query(StateFilter(FSMMakeTransaction.select_direction),
                            F.data.in_(DIRECTION))
async def process_button_press(callback: CallbackQuery, state: FSMContext):
    keyboard = create_inline_kb(4, **GAIN_CATEGORIES)
    await callback.message.edit_text(LexiconRu.select_category,
                                  reply_markup=keyboard)
    await callback.answer()
    await state.set_state(FSMMakeTransaction.select_category)


@user_router.callback_query(StateFilter(FSMMakeTransaction.select_category,
                                        F.data.in_(['prepayment', 'salary'])))
async def process_button_press_category(
        callback: CallbackQuery, state: FSMContext):
    category = callback.message.text
    user_dct = await state.get_data()
    logger.info(user_dct)
