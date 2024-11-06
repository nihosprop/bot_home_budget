import logging

from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import (CallbackQuery, Message)
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from database.db import database
from keyboards.keyboards import (kb_direction,
                                 kb_expenses_categories,
                                 kb_gain_categories)
from filters.filters import IsNumber
from lexicon.lexicon_ru import GAIN_CATEGORIES, LexiconRu
from states.states import FSMMakeTransaction
from utils.utils import add_income_in_db

logger = logging.getLogger(__name__)
user_router = Router()


# default_state
@user_router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(LexiconRu.start)
    await state.set_state(FSMMakeTransaction.fill_number)


# not default_state -> cancel
@user_router.callback_query(F.data == '/cancel', ~StateFilter(default_state))
async def process_cancel_command_state(
        clbk: CallbackQuery, state: FSMContext):
    await clbk.message.delete()
    await clbk.message.answer(LexiconRu.waiting_number)
    await clbk.answer()
    await state.set_state(FSMMakeTransaction.fill_number)


# state fill_number
@user_router.message(StateFilter(FSMMakeTransaction.fill_number), IsNumber())
async def process_number_sent(
        message: Message, state: FSMContext, number: dict[str, int | float]):
    await state.update_data(amount=number)
    await message.answer(LexiconRu.select_direction, reply_markup=kb_direction)
    await state.set_state(FSMMakeTransaction.select_direction)


@user_router.message(StateFilter(FSMMakeTransaction.fill_number))
async def sent_invalid_number(message: Message):
    await message.answer(f'{LexiconRu.other_message}')


# select_direction_income
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_direction),
                            F.data == 'income')
async def button_press_income(
        clbk: CallbackQuery, state: FSMContext):
    await clbk.message.edit_text(LexiconRu.select_category,
                                 reply_markup=kb_gain_categories)
    await clbk.answer()
    await state.set_state(FSMMakeTransaction.select_income)

# invalid_direction
@user_router.message(StateFilter(FSMMakeTransaction.select_direction))
async def invalid_select_direction(message: Message):
    await message.answer(text='Выберите направление', reply_markup=kb_direction)


# income_select_category
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_income),
                            F.data.in_(GAIN_CATEGORIES))
async def process_income_categories(clbk: CallbackQuery, state: FSMContext):
    await add_income_in_db(clbk, state)
    await clbk.message.edit_text(f'{LexiconRu.transaction_recorded}\n'
                                 f'{LexiconRu.waiting_number}')
    logger.info(f'{database}')
    await clbk.answer()
    await state.set_state(FSMMakeTransaction.fill_number)

# invalid_category
@user_router.message(StateFilter(FSMMakeTransaction.select_income))
async def invalid_income_categories(message: Message):
    await message.answer(text='Выберите категорию',
                         reply_markup=kb_gain_categories)
