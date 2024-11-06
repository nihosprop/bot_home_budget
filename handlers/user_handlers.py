import logging

from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import (CallbackQuery, Message)
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from database.db import database
from keyboards.keyboards import kb_direction, kb_gain_categories
from filters.filters import IsNumber
from lexicon.lexicon_ru import GAIN_CATEGORIES, LexiconRu, EXPENSES_CATEGORIES
from states.states import FSMMakeTransaction
from utils.utils import add_income_data_in_db

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
        callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(LexiconRu.waiting_number)
    await callback.answer()
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


# select_direction
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_direction),
                            F.data == 'income')
async def button_press_gain(
        callback: CallbackQuery, state: FSMContext):

    # delete_old_messages!
    await callback.message.edit_text(LexiconRu.select_category,
                                     reply_markup=kb_gain_categories)
    await callback.answer()
    await state.set_state(FSMMakeTransaction.select_category)

@user_router.message(StateFilter(FSMMakeTransaction.select_direction))
async def sent_invalid_select_direction(message: Message):
    # logger.info(message.model_dump_json(indent=4, exclude_defaults=True))
    await message.answer(text='Выберите направление', reply_markup=kb_direction)


# income_select_category
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_category),
                            F.data.in_(GAIN_CATEGORIES))
async def press_gain_categories(clbk: CallbackQuery, state: FSMContext):
    await add_income_data_in_db(clbk, state)
    await clbk.message.edit_text(f'{LexiconRu.transaction_recorded}\n'
                                 f'{LexiconRu.waiting_number}')
    logger.info(f'{database}')
    await clbk.answer()
    await state.set_state(FSMMakeTransaction.fill_number)

@user_router.message(StateFilter(FSMMakeTransaction.select_category))
async def process_invalid_gain_categories(message: Message):
    await message.answer(text='Выберите категорию',
                         reply_markup=kb_gain_categories)
