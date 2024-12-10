import logging

from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from database.db_utils import (add_expenses_in_db,
                               add_income_in_db,
                               add_user_in_db,
                               generate_fin_stats,
                               remove_user_from_db,
                               reset_month_stats)
from keyboards.keyboards import (kb_direction,
                                 kb_expenses_categories,
                                 kb_for_wait_amount,
                                 kb_income_categories,
                                 kb_reset_month_stats,
                                 kb_yes_cancel,
                                 kbs_for_expenses)
from filters.filters import IsNumber
from lexicon.lexicon_ru import (EXPENSES_CATEG_BUTT,
                                EXPENSE_SUBCATEGORY_BUTT,
                                INCOME_CATEG_BUTT,
                                LexiconRu,
                                MAP)
from states.states import FSMDeleteUser, FSMMakeTransaction
from utils.utils import MessageProcessor

user_router = Router()
logger_user_hand = logging.getLogger(__name__)


# cmd_start
@user_router.message(F.text == '/start')
async def cmd_start_default_state(msg: Message, state: FSMContext):
    logger_user_hand.debug('Entry')
    # remove msg '/start' from the user
    await add_user_in_db(str(msg.from_user.id))
    msg_processor = MessageProcessor(msg, state)
    await msg_processor.deletes_messages(msgs_for_del=True)
    value = await msg.answer(LexiconRu.await_amount,
                             reply_markup=kb_for_wait_amount)
    await msg_processor.save_msg_id(value, msgs_for_del=True)

    logger_user_hand.debug('Exit')


# reset user month stats
@user_router.callback_query(F.data == 'reset_month_stats')
async def clbk_reset_month(clbk: CallbackQuery, state: FSMContext):
    logger_user_hand.debug(f'{clbk.message.message_id=}')
    value = await clbk.message.edit_text(LexiconRu.text_confirm_reset_month,
                                         reply_markup=kb_reset_month_stats)
    await MessageProcessor(clbk, state).save_msg_id(value, msgs_for_del=True)
    await clbk.answer()


# confirm reset month stats
@user_router.callback_query(F.data == '/reset')
async def confirm_reset_month_stats(clbk: CallbackQuery, state: FSMContext):
    logger_user_hand.debug(f'{clbk.message.message_id=}')
    await reset_month_stats(clbk)
    value = await clbk.message.edit_text(LexiconRu.text_statistics_reset,
                                         reply_markup=kb_for_wait_amount)
    await MessageProcessor(clbk, state).save_msg_id(value, msgs_for_del=True)
    await clbk.answer()


# remove user
@user_router.callback_query(F.data == 'delete_user_data')
async def cmd_delete_user(clbk: Message, state: FSMContext):
    value = await clbk.message.edit_text(LexiconRu.text_confirm_del_data,
                                         reply_markup=kb_yes_cancel)
    await MessageProcessor(clbk, state).save_msg_id(value, msgs_for_del=True)
    await state.set_state(FSMDeleteUser.confirm_deletion)


# invalid confirm user
@user_router.message(StateFilter(FSMDeleteUser.confirm_deletion))
async def invalid_confirm_user(msg: Message):
    await msg.delete()


# confirm remove user
@user_router.callback_query(F.data == 'yes',
                            StateFilter(FSMDeleteUser.confirm_deletion))
async def confirm_remove_user(clbk: CallbackQuery, state: FSMContext):
    await remove_user_from_db(str(clbk.from_user.id))
    await clbk.message.edit_text(LexiconRu.text_del_success_data)
    await state.clear()


# cancel -> default_state
@user_router.callback_query(F.data == '/cancel')
async def cmd_cancel_no_state(clbk: CallbackQuery, state: FSMContext):
    value = await clbk.message.edit_text(LexiconRu.await_amount,
                                         reply_markup=kb_for_wait_amount)
    await MessageProcessor(clbk, state).save_msg_id(value, msgs_for_del=True)
    await state.set_state()
    await clbk.answer()


# cmd_report
@user_router.callback_query(F.data == '/report')
async def cmd_report(clbk: CallbackQuery, state: FSMContext):
    msg_processor: MessageProcessor = MessageProcessor(clbk, state)
    await msg_processor.removes_inline_kb()
    await msg_processor.deletes_messages(msgs_for_del=True)
    kb = clbk.message.reply_markup
    value = await clbk.message.answer(
            f'{await generate_fin_stats(clbk)}\n{LexiconRu.await_amount}',
            reply_markup=kb)
    await msg_processor.save_msg_id(value, msgs_remove_kb=True)
    await clbk.answer()


# cmd_categories
@user_router.callback_query(F.data == '/category')
async def cmd_show_categories(clbk: CallbackQuery, state: FSMContext):
    msg_processor: MessageProcessor = MessageProcessor(clbk, state)
    await msg_processor.deletes_messages(msgs_for_del=True)
    await msg_processor.removes_inline_kb()
    kb = clbk.message.reply_markup
    value = await clbk.message.answer(f'<pre>{MAP}</pre>\n'
                                      f'{LexiconRu.await_amount}',
                                      reply_markup=kb)
    await msg_processor.save_msg_id(value, msgs_remove_kb=True,
                                    msgs_for_del=True)
    await clbk.answer()


# fill_number
@user_router.message(IsNumber())
async def process_number_sent(
        msg: Message, state: FSMContext, number: bool | int | float):
    logger_user_hand.debug('Entry')

    msg_processor = MessageProcessor(msg, state)
    await msg_processor.deletes_messages(msgs_for_del=True)
    await msg_processor.removes_inline_kb()
    await state.hset(amount=number)
    await msg.answer(LexiconRu.select_direction, reply_markup=kb_direction)
    await state.set_state(FSMMakeTransaction.select_direction)

    logger_user_hand.debug('Exit')


# invalid number
@user_router.message(StateFilter(default_state))
async def process_invalid_number(msg: Message):
    await msg.delete()


# select_income_direction
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_direction),
                            F.data == 'income')
async def button_press_income(clbk: CallbackQuery, state: FSMContext):
    await clbk.message.edit_text(LexiconRu.select_category,
                                 reply_markup=kb_income_categories)
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
    await msg_processor.deletes_messages(msgs_for_del=True)
    value = await clbk.message.edit_text(f'{LexiconRu.transaction_recorded}\n'
                                         f'{await generate_fin_stats(clbk)}'
                                         f'{LexiconRu.await_amount}',
                                         reply_markup=kb_for_wait_amount)
    await msg_processor.save_msg_id(value, msgs_for_del=True)
    await state.set_state()
    await clbk.answer()


# invalid_category
@user_router.message(StateFilter(FSMMakeTransaction.select_income))
async def invalid_income_category(msg: Message):
    await msg.delete()


# expenses_click
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_direction),
                            F.data == 'expenses')
async def button_press_expenses(clbk: CallbackQuery, state: FSMContext):
    await clbk.message.edit_text(LexiconRu.select_category,
                                 reply_markup=kb_expenses_categories)
    await state.set_state(FSMMakeTransaction.select_expenses)
    await clbk.answer()


# select_expenses
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_expenses),
                            F.data.in_(EXPENSES_CATEG_BUTT))
async def expenses_categ_click(clbk: CallbackQuery, state: FSMContext):
    logger_user_hand.debug('Entry')
    category = clbk.data
    await state.update_data(category=category)
    await clbk.message.edit_text(LexiconRu.select_category,
                                 reply_markup=kbs_for_expenses[category])
    await state.set_state(FSMMakeTransaction.select_subcategory)
    await clbk.answer()
    logger_user_hand.debug('Exit')


# invalid select expenses
@user_router.message(StateFilter(FSMMakeTransaction.select_expenses))
async def invalid_expenses_categories(msg: Message):
    await msg.delete()


# select subcategories
@user_router.callback_query(StateFilter(FSMMakeTransaction.select_subcategory,
                                        F.data.in_(
                                                EXPENSE_SUBCATEGORY_BUTT.values())))
async def press_subcategory(clbk: CallbackQuery, state: FSMContext):
    logger_user_hand.debug('Entry')
    await add_expenses_in_db(clbk, state)
    msg_processor = MessageProcessor(clbk, state)
    value = await clbk.message.edit_text(f'{LexiconRu.transaction_recorded}\n'
                                         f'{await generate_fin_stats(clbk)}'
                                         f'{LexiconRu.await_amount}',
                                         reply_markup=kb_for_wait_amount)
    await msg_processor.deletes_messages(msgs_for_del=True)
    await msg_processor.save_msg_id(value, msgs_for_del=True)
    await state.set_state()
    await clbk.answer()
    logger_user_hand.debug('Exit')


# invalid select subcategory
@user_router.message(StateFilter(FSMMakeTransaction.select_subcategory))
async def invalid_subcategory(msg: Message):
    await msg.delete()
