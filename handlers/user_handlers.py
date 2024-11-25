import logging

from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import (CallbackQuery, Message)
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from database.db import database
from database.db_utils import (add_expenses_in_db,
                               add_income_in_db,
                               add_user_in_db,
                               generate_fin_stats,
                               remove_user_from_db,
                               reset_stats)
from keyboards.keyboards import (kb_direction,
                                 kb_expenses_categories,
                                 kb_for_wait_amount,
                                 kb_income_categories,
                                 kb_reset_month_stats,
                                 kb_yes_cancel,
                                 kbs_for_expenses)
from filters.filters import IsNumber
from lexicon.lexicon_ru import (EXPENSES_CATEG_BUTT,
                                EXPENSE_SUBCATEGORY_BUTTONS,
                                INCOME_CATEG_BUTT,
                                LexiconRu,
                                MAP)
from states.states import FSMMakeTransaction
from utils.utils import MessageProcessor

user_router = Router()
logger_user_hand = logging.getLogger(__name__)

format_1 = (
        '[{asctime}] #{levelname:<8} {filename:<17}:{lineno:4} - <{funcName}> '
        '- {message}')
formatter1 = logging.Formatter(fmt=format_1, datefmt='%Y.%m.%d %H:%M:%S',
                               style='{')
file_handler = logging.FileHandler('logs/logs.log', mode='w', encoding='utf-8')
file_handler.setFormatter(formatter1)
logger_user_hand.addHandler(file_handler)


# cmd_start_default_state
@user_router.message(CommandStart(), StateFilter(default_state))
async def cmd_start_default_state(msg: Message, state: FSMContext):
    await add_user_in_db(msg)
    await msg.answer(LexiconRu.start)
    await state.set_state(FSMMakeTransaction.fill_number)
    await state.update_data(msg_for_del=set())


# reset user month stats
@user_router.callback_query(F.data == 'reset_month_stats',
                            ~StateFilter(default_state))
async def clbk_reset_month(clbk: CallbackQuery):
    logger_user_hand.debug(f'{database=}')
    await clbk.message.edit_text('Подтвердите сброс статистики за месяц.\n'
                                 'Общий баланс затронут не будет.',
                                 reply_markup=kb_reset_month_stats)
    await clbk.answer()


# confirm reset month stats
@user_router.callback_query(F.data == '/reset', ~StateFilter(default_state))
async def confirm_reset_month_stats(clbk: CallbackQuery):
    await reset_stats(clbk)
    logger_user_hand.info(f'Monthly statistics for {clbk.from_user.id} reset')
    await clbk.message.edit_text(LexiconRu.text_statistics_reset,
                                 reply_markup=kb_for_wait_amount)
    await clbk.answer()


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
    msg_processor: MessageProcessor = MessageProcessor(clbk, state)
    value = await clbk.message.edit_text(LexiconRu.await_amount,
                                         reply_markup=kb_for_wait_amount)
    logger_user_hand.debug(f'{value.__class__=}')
    await msg_processor.writes_msg_id_to_storage(value)
    await state.set_state(FSMMakeTransaction.fill_number)
    await clbk.answer()


# region important(__int__)
# cmd_report
@user_router.callback_query(F.data == '/report',
                            StateFilter(FSMMakeTransaction.fill_number))
async def cmd_report(clbk: CallbackQuery, state: FSMContext):
    msg_processor: MessageProcessor = MessageProcessor(clbk, state)
    await msg_processor.removes_inline_msg_kb()
    await msg_processor.deletes_messages()
    kb = clbk.message.reply_markup
    value = await clbk.message.answer(await generate_fin_stats(clbk,
                                                               database) +
                                      '\n' + LexiconRu.await_amount,
            reply_markup=kb)
    await msg_processor.writes_msg_id_to_storage(value, key='msg_ids_remove_kb')
    await clbk.answer()


# cmd_categories
@user_router.callback_query(F.data == '/category',
                            StateFilter(FSMMakeTransaction.fill_number))
async def cmd_show_categories(clbk: CallbackQuery, state: FSMContext):
    msg_processor: MessageProcessor = MessageProcessor(clbk, state)
    await msg_processor.deletes_messages()
    await msg_processor.removes_inline_msg_kb()
    kb = clbk.message.reply_markup
    value = await clbk.message.answer(f'<pre>{MAP}</pre>\n'
                                      f'{LexiconRu.await_amount}',
                                      reply_markup=kb)

    await msg_processor.writes_msg_id_to_storage(value, 'msg_ids_remove_kb')
    await clbk.answer()


# state fill_number
@user_router.message(StateFilter(FSMMakeTransaction.fill_number), IsNumber())
async def process_number_sent(
        msg: Message, state: FSMContext, number: bool | int | float):
    msg_processor = MessageProcessor(msg, state)
    updates = await msg.bot.get_updates()
    logger_user_hand.debug(f'{bool(updates)=}')
    await msg_processor.deletes_messages()
    await msg_processor.removes_inline_msg_kb()
    logger_user_hand.debug(f'{bool(updates)=}')

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
    msg_processor = MessageProcessor(clbk, state)
    await msg_processor.deletes_messages()
    value = await clbk.message.edit_text(f'{LexiconRu.transaction_recorded}\n'
                                         f'{LexiconRu.await_amount}',
                                         reply_markup=kb_for_wait_amount)
    logger_user_hand.debug(database)
    await msg_processor.writes_msg_id_to_storage(value)
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
    await clbk.message.edit_text(LexiconRu.select_category,
                                 reply_markup=kbs_for_expenses[category])
    await state.set_state(FSMMakeTransaction.select_subcategory)
    await clbk.answer()


# invalid select expenses
@user_router.message(StateFilter(FSMMakeTransaction.select_expenses))
async def invalid_expenses_categories(msg: Message):
    await msg.delete()


# select subcategories
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_subcategory,
                                        F.data.in_(
                                                EXPENSE_SUBCATEGORY_BUTTONS.values())))
async def press_subcategory(clbk: CallbackQuery, state: FSMContext):
    await add_expenses_in_db(clbk, state)
    value = await clbk.message.edit_text(f'{LexiconRu.transaction_recorded}\n'
                                         f'{LexiconRu.await_amount}',
                                         reply_markup=kb_for_wait_amount)
    logger_user_hand.debug(f'{database}')
    msg_processor = MessageProcessor(clbk, state)
    await msg_processor.deletes_messages()
    await msg_processor.writes_msg_id_to_storage(value)
    await state.set_state(FSMMakeTransaction.fill_number)
    await clbk.answer()


# invalid select subcategory
@user_router.message(StateFilter(FSMMakeTransaction.select_subcategory))
async def invalid_subcategory(msg: Message):
    await msg.delete()
