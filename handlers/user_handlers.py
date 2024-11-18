import logging

from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import (CallbackQuery, Message)
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from database.db import database
from keyboards.keyboards import (kb_direction,
                                 kb_expenses_categories,
                                 kb_income_categories,
                                 kb_for_wait_amount,
                                 kb_yes_cancel,
                                 kbs_for_expenses)
from filters.filters import IsNumber
from lexicon.lexicon_ru import (EXPENSES_CATEG_BUTT,
                                EXPENSE_SUBCATEGORY_BUTTONS,
                                INCOME_CATEG_BUTT,
                                LexiconRu,
                                MAP)
from states.states import FSMMakeTransaction
from utils.utils import (add_expenses_in_db,
                         add_income_in_db,
                         add_user_in_db,
                         generate_fin_report,
                         remove_user_from_db)

logger_user_hand = logging.getLogger(__name__)
user_router = Router()


# default_state
@user_router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(msg: Message, state: FSMContext):
    await add_user_in_db(msg)
    logger_user_hand.info(database)
    await msg.answer(LexiconRu.start)
    await state.set_state(FSMMakeTransaction.fill_number)
    await state.update_data(msg_for_del=set())


# remove user
@user_router.message(F.text == '/delete_user', ~StateFilter(default_state))
async def cmd_delete_user(msg: Message):
    await msg.answer('Подтвердить удаление данных!', reply_markup=kb_yes_cancel)


# confirm remove user
@user_router.callback_query(F.data == 'yes')
async def confirm_remove_user(clbk: CallbackQuery, state: FSMContext):
    user_id = str(clbk.from_user.id)
    await remove_user_from_db(user_id)
    await clbk.message.edit_text(LexiconRu.text_confirm_remove)
    await state.clear()

# cancel -> ~default_state
@user_router.callback_query(F.data == '/cancel', ~StateFilter(default_state))
async def cmd_cancel_in_state(
        clbk: CallbackQuery, state: FSMContext):
    value = await clbk.message.edit_text(LexiconRu.await_amount,
                                         reply_markup=kb_for_wait_amount)

    msg_for_del: set = dict(await state.get_data()).get('msg_for_del', set())
    for msg_id in msg_for_del:
        try:
            await clbk.bot.delete_message(chat_id=clbk.message.chat.id,
                                          message_id=msg_id)
        except TelegramBadRequest as err:
            logger_user_hand.error(f'Failed to remove inline keyboard: {err}')
    await state.update_data(msg_for_del=set())

    msg_for_del: set[int] = dict(await state.get_data()).get('msg_for_del',
                                                             set())
    msg_for_del.add(value.message_id)
    await state.update_data(msg_for_del=msg_for_del)

    await state.set_state(FSMMakeTransaction.fill_number)
    await clbk.answer()


# region important(__int__)
# cmd_report
@user_router.callback_query(F.data == '/report',
                            StateFilter(FSMMakeTransaction.fill_number))
async def cmd_report(clbk: CallbackQuery, state: FSMContext):
    msg_id = dict(await state.get_data()).get('msg_record_trans')
    logger_user_hand.info(msg_id)
    if msg_id:
        await clbk.message.delete()
    await clbk.message.answer(text=await generate_fin_report(clbk,
                                                             database) + '\n' + LexiconRu.await_amount)


# default_state -> cancel
@user_router.message(F.text == '/cancel', StateFilter(default_state))
async def cmd_cancel_in_state(msg: Message):
    await msg.delete()
    await msg.answer(f'Сейчас нечего отменять.\n'
                     f'{LexiconRu.await_start}')


# cmd_categories
@user_router.callback_query(F.data == '/category', StateFilter(
        FSMMakeTransaction.fill_number))
async def cmd_show_categories(clbk: CallbackQuery):
    kb = clbk.message.reply_markup
    await clbk.message.answer(f'<code>{MAP}</code>\n{LexiconRu.await_amount}',
                              reply_markup=kb)


# state fill_number
@user_router.message(StateFilter(FSMMakeTransaction.fill_number), IsNumber())
async def process_number_sent(
        msg: Message, state: FSMContext, number: dict[str, int | float]):
    await state.update_data(amount=number)
    await msg.answer(LexiconRu.select_direction, reply_markup=kb_direction)
    await state.set_state(FSMMakeTransaction.select_direction)


# invalid number
@user_router.message(StateFilter(FSMMakeTransaction.fill_number))
async def sent_invalid_number(msg: Message):
    await msg.delete()


# endregion

# select_income_direction
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_direction),
                            F.data == 'income')
async def button_press_income(
        clbk: CallbackQuery, state: FSMContext):
    value = await clbk.message.edit_text(LexiconRu.select_category,
                                         reply_markup=kb_income_categories)
    await state.update_data(msg_id_income_categ=value.message_id)
    await state.set_state(FSMMakeTransaction.select_income)
    await clbk.answer()


# invalid_direction
@user_router.message(StateFilter(FSMMakeTransaction.select_direction))
async def invalid_select_direction(msg: Message):
    await msg.delete()


# select_income_category
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_income),
                            F.data.in_(INCOME_CATEG_BUTT))
async def process_income_categories(clbk: CallbackQuery, state: FSMContext):
    await add_income_in_db(clbk, state)
    value = await clbk.message.edit_text(f'{LexiconRu.transaction_recorded}\n'
                                         f'{LexiconRu.await_amount}',
                                         reply_markup=kb_for_wait_amount)
    logger_user_hand.info(database)
    msg_for_del: set[int] = dict(await state.get_data()).get('msg_for_del',
                                                             set())

    for msg_id in msg_for_del:
        try:
            await clbk.bot.delete_message(chat_id=clbk.message.chat.id,
                                          message_id=msg_id)
        except TelegramBadRequest as err:
            logger_user_hand.error(f'Failed to remove inline keyboard: {err}')
    await state.update_data(msg_for_del=set())

    msg_for_del: set[int] = dict(await state.get_data()).get('msg_for_del',
                                                             set())
    msg_for_del.add(value.message_id)
    await state.update_data(msg_for_del=msg_for_del)

    await state.set_state(FSMMakeTransaction.fill_number)
    await clbk.answer()


# invalid_category
@user_router.message(StateFilter(FSMMakeTransaction.select_income))
async def invalid_income_category(msg: Message):
    await msg.delete()


# expenses_click
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_direction),
                            F.data == 'expenses')
async def button_press_expenses(
        clbk: CallbackQuery, state: FSMContext):
    await clbk.message.edit_text(LexiconRu.select_category,
                                 reply_markup=kb_expenses_categories)
    await state.set_state(FSMMakeTransaction.select_expenses)
    await clbk.answer()


# select_expenses
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_expenses),
                            F.data.in_(EXPENSES_CATEG_BUTT))
async def expenses_categ_click(clbk: CallbackQuery, state: FSMContext):
    category = clbk.data
    await state.update_data(category=category)
    await clbk.message.edit_text('Выберите категорию',
                                 reply_markup=kbs_for_expenses[category])
    await state.set_state(FSMMakeTransaction.select_subcategory)
    await clbk.answer()


# invalid select expenses
@user_router.message(StateFilter(FSMMakeTransaction.select_expenses))
async def invalid_expenses_categories(msg: Message):
    await msg.delete()


# select subcategories
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_subcategory,
                                        F.data.in_(EXPENSE_SUBCATEGORY_BUTTONS.values())))
async def press_subcategory(clbk: CallbackQuery, state: FSMContext):
    await add_expenses_in_db(clbk, state)
    value = await clbk.message.edit_text(f'{LexiconRu.transaction_recorded}\n'
                                         f'{LexiconRu.await_amount}',
                                         reply_markup=kb_for_wait_amount)
    logger_user_hand.info(f'{database}')
    msg_for_del: set[int] = dict(await state.get_data()).get('msg_for_del',
                                                             set())

    for msg_id in msg_for_del:
        try:
            await clbk.bot.delete_message(chat_id=clbk.message.chat.id,
                                          message_id=msg_id)
        except TelegramBadRequest as err:
            logger_user_hand.error(f'Failed to remove inline keyboard: {err}')

    await state.update_data(msg_for_del=set())

    msg_for_del: set[int] = dict(await state.get_data()).get('msg_for_del',
                                                             set())
    msg_for_del.add(value.message_id)
    await state.update_data(msg_for_del=msg_for_del)

    await state.set_state(FSMMakeTransaction.fill_number)
    await clbk.answer()


# invalid select subcategory
@user_router.message(StateFilter(FSMMakeTransaction.select_subcategory))
async def invalid_subcategory(msg: Message):
    await msg.delete()
