import json
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.fsm.storage.redis import Redis

from lexicon.lexicon_ru import (EXPENSE_SUBCATEGORY_BUTT,
                                EXPENSES_CATEG_BUTT,
                                INCOME_CATEG_BUTT)

logger_db_utils = logging.getLogger(__name__)
db = Redis(host='localhost', port=6379, db=1)


async def set_data_json(path: str = 'database/db.json'):
    keys = await db.keys()
    all_data: dict = {}

    for key in keys:
        value = await db.get(key)
        deserialized_value: dict = json.loads(value.decode('utf-8'))
        all_data[key.decode('utf-8')] = deserialized_value

    with open(path, 'w') as file:
        json.dump(all_data, file, indent=4)


async def get_data_json(path: str = 'database/db.json'):

    with open(path, 'r') as file:
        data = json.load(file)
    # Cleaning up the current Redis database
    await db.flushdb()
    for user_id, user_info in data.items():
        await db.set(user_id, json.dumps(user_info))


async def remove_user_from_db(user_id: str):
    await db.delete(user_id)
    await set_data_json()


async def add_user_in_db(user_id: str) -> None:
    logger_db_utils.debug('Entry')
    data_user = await db.get(user_id)
    logger_db_utils.debug(f'{data_user=}')

    if not data_user:
        user_dict = {'balance': 0, 'income': {}, 'expenses': {}}
        await db.set(user_id, json.dumps(user_dict))
        await set_data_json()

    logger_db_utils.debug('Exit')


async def reset_month_stats(clbk: CallbackQuery) -> None:
    """Resets statistics on request for only a month."""
    logger_db_utils.debug('Entry')

    user_id = str(clbk.from_user.id)
    user_data = await db.get(user_id)
    user_data_dict = json.loads(user_data.decode('utf-8'))
    user_data_dict['income'] = {}
    user_data_dict['expenses'] = {}
    await db.set(user_id, json.dumps(user_data_dict))
    await set_data_json()
    logger_db_utils.info(f'Monthly statistics for {clbk.from_user.id} reset')
    logger_db_utils.debug('Exit')

async def _calc_percent(
        amount: int | float, num: int | float) -> str:
    if amount:
        return f'({round(num * 100 / amount, 1)}%)'
    return ''

async def add_income_in_db(clbk: CallbackQuery, state: FSMContext) -> None:
    logger_db_utils.debug('Entry')

    category = clbk.data
    user_id = str(clbk.from_user.id)
    user_data = await db.get(user_id)

    if not user_data:
        await add_user_in_db(user_id)

    user_data_dict = json.loads(user_data.decode('utf-8'))

    data = await state.get_data()

    logger_db_utils.debug(f'{data=}')
    amount = data.get('amount')
    logger_db_utils.debug(f'{amount=}')

    try:
        user_data_dict['balance'] += amount
    except Exception as err:
        logger_db_utils.error(f'{err=}')
    try:
        user_data_dict['income'][category] = (
                user_data_dict['income'].setdefault(category, 0) + amount)
    except Exception as err:
        logger_db_utils.error(f'{err=}')
    logger_db_utils.debug('Exit')
    await db.set(user_id, json.dumps(user_data_dict))
    await set_data_json()

    logger_db_utils.debug('Entry')


async def add_expenses_in_db(
        clbk: CallbackQuery, state: FSMContext) -> None:
    logger_db_utils.debug('Entry')

    user_id = str(clbk.from_user.id)
    data = await state.get_data()
    amount = data.get('amount')
    category = data['category']
    subcategory = clbk.data

    user_data = await db.get(user_id)
    user_data_dict = json.loads(user_data.decode('utf-8'))
    user_data_dict['balance'] -= amount
    user_data_dict['expenses'][category][subcategory] = (
            user_data_dict['expenses'].setdefault(category, {}).setdefault(
                    subcategory, 0) + amount)
    logger_db_utils.debug('Exit')
    await db.set(user_id, json.dumps(user_data_dict))
    await set_data_json()


async def generate_fin_stats(clbk: CallbackQuery) -> str:
    date: str = clbk.message.date.strftime('%d.%m.%Y %H:%M (UTC)')
    user_id = str(clbk.from_user.id)
    logger_db_utils.debug(f'Entry\n{date=}:{user_id=}')
    user_data = await db.get(user_id)
    user_data_dict = json.loads(user_data.decode('utf-8'))

    monthly_income = user_data_dict['income']
    sum_income = sum(monthly_income.values())
    balance: int | float = user_data_dict['balance']
    expenses: dict[str, dict[str, float | int]] = user_data_dict['expenses']
    sum_expenses = sum(
            sum(obj) for obj in (categ.values() for categ in expenses.values()))

    report: str = (f'<u><i>{date}</i></u>\n\n'
                   f'<b>Баланс: </b>{balance}\n'
                   f'<b>Сальдо:</b>'
                   f' {balance - sum_expenses}\n'
                   f'------------------------\n'
                   f'<b>Доходы за месяц:</b> {sum_income}\n')

    for category, value in monthly_income.items():
        report += f'  - {INCOME_CATEG_BUTT[category]}: {value}\n'
    report += (f'<b>------------------------\n'
               f'Расходы за месяц: {round(sum_expenses, 2)}</b>\n')

    for category, data in expenses.items():
        report += f'  {EXPENSES_CATEG_BUTT[category]}:\n'
        for subcategory, value in data.items():

            report += (f'    - {EXPENSE_SUBCATEGORY_BUTT[subcategory]}: '
                       f'{value}{await _calc_percent(sum_income, value)}\n')
    logger_db_utils.debug('Exit')
    return f'<code>{report}</code>'
