import logging

from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import (CallbackQuery, Message)
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from filters.filters import IsNumber
from keyboards.keyboard_utils import create_inline_kb
from lexicon.lexicon_ru import DIRECTION, GAIN_CATEGORIES, LexiconRu
from states.states import FSMMakeTransaction

logger = logging.getLogger(__name__)
user_router = Router()
user_dict = {}


@user_router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer(LexiconRu.start)
    await state.set_state(FSMMakeTransaction.fill_number)


@user_router.callback_query(F.data == '/cancel', ~StateFilter(default_state))
async def process_cancel_command_state(
        callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(LexiconRu.waiting_number)
    await callback.answer()
    await state.set_state(FSMMakeTransaction.fill_number)


# fill_number
@user_router.message(StateFilter(FSMMakeTransaction.fill_number), IsNumber())
async def process_number_sent(
        message: Message, state: FSMContext, number: dict[str, int | float]):
    keyboard = create_inline_kb(2, **DIRECTION)
    await state.update_data(amount=number)
    await message.answer(LexiconRu.select_direction, reply_markup=keyboard)
    await state.set_state(FSMMakeTransaction.select_direction)


@user_router.message(StateFilter(FSMMakeTransaction.fill_number))
async def process_invalid_number(message: Message):
    await message.answer(f'{LexiconRu.other_message}')


# select_direction
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_direction),
                            F.data == 'gain')
async def button_press_gain(
        callback: CallbackQuery, state: FSMContext):
    keyboard = create_inline_kb(2, **GAIN_CATEGORIES)
    await callback.message.edit_text(LexiconRu.select_category,
                                     reply_markup=keyboard)
    await callback.answer()
    await state.set_state(FSMMakeTransaction.select_category)


@user_router.message(StateFilter(FSMMakeTransaction.select_direction))
async def process_invalid_select_direction(message: Message, state: FSMContext):
    # остается сообщение 'Выберите направление' надо его убрать
    await message.answer(text='Выберите направление')


# select_category
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_category),
                            F.data.in_(GAIN_CATEGORIES))
async def press_bt_gain_categories(callback: CallbackQuery, state: FSMContext):
    category = callback.data
    dct = await state.get_data()
    amount = dct['amount']
    logger.info(f'переменная {amount=}')
    user_dict.setdefault(str(callback.from_user.id), {
            'gain': {
                    category: 0}})
    user_dict[str(callback.from_user.id)]['gain'][category] += amount

    await callback.message.edit_text(f'{LexiconRu.transaction_recorded}\n'
                                     f'{LexiconRu.waiting_number}')
    logger.info(f'{user_dict}')
    await callback.answer()
    await state.set_state(FSMMakeTransaction.fill_number)


@user_router.message(StateFilter(FSMMakeTransaction.select_category))
async def process_invalid_gain_categories(message: Message):
    await message.answer(text='Выберите категорию')
