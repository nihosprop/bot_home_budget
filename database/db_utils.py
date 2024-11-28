import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from lexicon.lexicon_ru import (EXPENSE_SUBCATEGORY_BUTTONS,
                                EXPENSES_CATEG_BUTT,
                                INCOME_CATEG_BUTT)
from utils.utils import logger_utils
from database.db import database
logger_db_utils = logging.getLogger(__name__)

async def remove_user_from_db(user_id: str):
    database.pop(user_id)

# move to middleware!!!
async def add_user_in_db(msg: Message) -> None:
    user_id = str(msg.from_user.id)
    if not database.get(user_id):
        database.setdefault(user_id, {'balance': 0, 'income': {}, 'expenses': {}})

async def reset_stats(clbk: CallbackQuery) -> None:
    """Resets statistics on request for only a month."""
    user_id = str(clbk.from_user.id)
    database[user_id].update({'income': {}, 'expenses': {}})
    logger_utils.debug(f'{user_id=}{database=}')

async def calc_percent(
        amount: int | float, num: int | float) -> str:
    if amount:
        return f'({round(num * 100 / amount, 1)}%)'
    return ''

async def add_income_in_db(
        clbk: CallbackQuery, state: FSMContext) -> None:
    category = clbk.data
    user_id = str(clbk.from_user.id)
    data = await state.get_data()
    amount = data['amount']
    database[user_id]['balance'] += amount
    database[user_id]['income'][category] = (
            database[user_id]['income'].setdefault(category, 0) + amount)


async def add_expenses_in_db(
        clbk: CallbackQuery, state: FSMContext) -> None:
    user_id = str(clbk.from_user.id)
    data = await state.get_data()
    amount = data['amount']
    category = data['category']
    subcategory = clbk.data
    database.setdefault(user_id, {'income': {}, 'expenses': {}})
    database[user_id]['expenses'][category][subcategory] = (
            database[user_id]['expenses'].setdefault(category, {}).setdefault(
                    subcategory,
                    0) + amount)


async def generate_fin_stats(clbk: CallbackQuery, data: dict) -> str:
    date: str = clbk.message.date.strftime('%d.%m.%Y %H:%M (UTC)')
    logger_db_utils.debug(f'{date=}')
    user_id = str(clbk.from_user.id)
    logger_db_utils.debug(f'{user_id=}')
    monthly_income: dict[str, float | int] = data[user_id]['income']
    sum_income = sum(monthly_income.values())
    balance: int | float = data[user_id]['balance']
    expenses: dict[str, dict[str, float | int]] = data[user_id]['expenses']
    sum_expenses = sum(
            sum(obj) for obj in (categ.values() for categ in expenses.values()))

    report: str = (f'<u><i>{date}</i></u>\n\n'
                   f'<b>Баланс: </b>{balance}\n'
                   f'<b>Сальдо:</b>'
                   f' {sum_income - sum_expenses}\n'
                   f'------------------------\n'
                   f'<b>Доходы за месяц:</b> {sum_income}\n')

    for category, value in monthly_income.items():
        report += f'  - {INCOME_CATEG_BUTT[category]}: {value}\n'
    report += (f'<b>------------------------\n'
               f'Расходы за месяц: {round(sum_expenses, 2)}</b>\n')

    for category, data in expenses.items():
        report += f'  {EXPENSES_CATEG_BUTT[category]}:\n'
        for subcategory, value in data.items():

            report += (f'    - {EXPENSE_SUBCATEGORY_BUTTONS[subcategory]}: '
                       f'{value}{await calc_percent(sum_income, value)}\n')

    return f'<code>{report}</code>'
