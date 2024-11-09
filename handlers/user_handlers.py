import logging

from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import (CallbackQuery, Message)
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from database.db import database
from keyboards.keyboards import (kb_direction,
                                 kb_expenses_categories,
                                 kb_income_categories)
from filters.filters import IsNumber
from lexicon.lexicon_ru import EXPENSES_CATEGORIES, INCOME_CATEGORIES, LexiconRu
from states.states import FSMMakeTransaction
from utils.utils import add_expenses_in_db, add_income_in_db

user_hand_logger = logging.getLogger(__name__)
user_router = Router()


# default_state
@user_router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(msg: Message, state: FSMContext):
    await msg.answer(LexiconRu.start)
    await state.set_state(FSMMakeTransaction.fill_number)


@user_router.message(F.text == '/help')
async def cmd_help(msg: Message, state: FSMContext):

    match await state.get_state():
        case FSMMakeTransaction.fill_number:
            await msg.answer(LexiconRu.help_state_fill_number)
        case FSMMakeTransaction.select_direction:
            await msg.answer(LexiconRu.help_state_direction,
                             reply_markup=kb_direction)
        case FSMMakeTransaction.select_income:
            await msg.answer(LexiconRu.help_state_categories,
                             reply_markup=kb_income_categories)
        case FSMMakeTransaction.select_expenses:
            await msg.answer(LexiconRu.help_state_categories,
                             reply_markup=kb_expenses_categories)
        case _:
            await msg.answer(LexiconRu.help_default_state)


# not default_state -> cancel
@user_router.callback_query(F.data == '/cancel', ~StateFilter(default_state))
async def process_cancel_command_state(
        clbk: CallbackQuery, state: FSMContext):
    await clbk.message.delete()
    await clbk.message.answer(LexiconRu.waiting_number)
    await clbk.answer()
    await state.set_state(FSMMakeTransaction.fill_number)

# default_state -> cancel
@user_router.callback_query(F.data == '/cancel', StateFilter(default_state))
async def cmd_cancel_in_state(clbk: CallbackQuery):
    await clbk.message.delete()
    await clbk.message.answer(f'Сейчас вам нечего отменять.\n'
                              f'{LexiconRu.await_start}')
    await clbk.answer()

# state fill_number
@user_router.message(StateFilter(FSMMakeTransaction.fill_number), IsNumber())
async def process_number_sent(
        msg: Message, state: FSMContext, number: dict[str, int | float]):
    await state.update_data(amount=number)
    await msg.answer(LexiconRu.select_direction, reply_markup=kb_direction)
    await state.set_state(FSMMakeTransaction.select_direction)


@user_router.message(StateFilter(FSMMakeTransaction.fill_number))
async def sent_invalid_number(msg: Message):
    await msg.answer(f'{LexiconRu.other_message}')


# select_direction_income
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_direction),
                            F.data == 'income')
async def button_press_income(
        clbk: CallbackQuery, state: FSMContext):
    await clbk.message.edit_text(LexiconRu.select_category,
                                 reply_markup=kb_income_categories)
    await clbk.answer()
    await state.set_state(FSMMakeTransaction.select_income)


# invalid_direction
@user_router.message(StateFilter(FSMMakeTransaction.select_direction))
async def invalid_select_direction(msg: Message):
    await msg.answer(text='Выберите направление', reply_markup=kb_direction)


# income_select_category
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_income),
                            F.data.in_(INCOME_CATEGORIES))
async def process_income_categories(clbk: CallbackQuery, state: FSMContext):
    await add_income_in_db(clbk, state)
    await clbk.message.edit_text(f'{LexiconRu.transaction_recorded}\n'
                                 f'{LexiconRu.waiting_number}')
    user_hand_logger.info(f'{database}')
    await clbk.answer()
    await state.set_state(FSMMakeTransaction.fill_number)


# invalid_category
@user_router.message(StateFilter(FSMMakeTransaction.select_income))
async def invalid_income_categories(msg: Message):
    await msg.answer(text='Выберите категорию',
                     reply_markup=kb_income_categories)


# select_direction_expenses
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_direction),
                            F.data == 'expenses')
async def button_press_expenses(
        clbk: CallbackQuery, state: FSMContext):
    await clbk.message.edit_text(LexiconRu.select_category,
                                 reply_markup=kb_expenses_categories)
    await clbk.answer()
    await state.set_state(FSMMakeTransaction.select_expenses)


# invalid_direction
@user_router.message(StateFilter(FSMMakeTransaction.select_direction))
async def invalid_select_direction(msg: Message):
    await msg.answer(text=LexiconRu.select_direction, reply_markup=kb_direction)


# expenses_select_category
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_expenses),
                            F.data.in_(EXPENSES_CATEGORIES))
async def process_expenses_categories(clbk: CallbackQuery, state: FSMContext):
    await add_expenses_in_db(clbk, state)
    await clbk.message.edit_text(f'{LexiconRu.transaction_recorded}\n'
                                 f'{LexiconRu.waiting_number}')
    user_hand_logger.info(f'{database}')
    await clbk.answer()
    await state.set_state(FSMMakeTransaction.fill_number)


# invalid_expenses
@user_router.message(StateFilter(FSMMakeTransaction.select_expenses))
async def invalid_income_categories(msg: Message):
    await msg.answer(text=LexiconRu.select_category,
                     reply_markup=kb_expenses_categories)
