import json
import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.fsm.storage.redis import Redis

from lexicon.lexicon_ru import (EXPENSES_CATEG_BUTT,
                                EXPENSE_SUBCATEGORY_BUTT,
                                INCOME_CATEG_BUTT)

logger_db_utils = logging.getLogger(__name__)
db1 = Redis(host='localhost', port=6379, db=1)


async def flush_redis_db():
    await db1.flushdb()


async def set_data_json(path: str = 'database/db.json'):
    """
    Saves all data from the Redis database to a JSON file.
    This method retrieves all keys and values from the Redis database,
    deserializes them and saves as a JSON object to a file.
    Args: path (str): Path to the file, where the data will be saved.
    The default is 'database/db.json'.
    :param path:
    :return: None
    """

    all_data: dict = {}
    for key in await db1.keys():
        value = await db1.get(key)
        deserialized_value: dict = json.loads(value.decode('utf-8'))
        all_data[key.decode('utf-8')] = deserialized_value

    with open(path, 'w') as file:
        json.dump(all_data, file, indent=4)


async def get_data_json(path: str = 'database/db.json'):

    with open(path, 'r') as file:
        data = json.load(file)
    for user_id, user_info in data.items():
        await db1.set(user_id, json.dumps(user_info))


async def remove_user_from_db(user_id: str):
    await db1.delete(user_id)
    await set_data_json()


async def add_user_in_db(user_id: str) -> None:
    logger_db_utils.debug('Entry')
    data_user = await db1.get(user_id)
    logger_db_utils.debug(f'{data_user=}')

    if not data_user:
        user_dict = {'balance': 0, 'income': {}, 'expenses': {}}
        await db1.set(user_id, json.dumps(user_dict))
        await set_data_json()

    logger_db_utils.debug('Exit')


async def reset_month_stats(clbk: CallbackQuery) -> None:
    """Resets statistics on request for only a month."""
    logger_db_utils.debug('Entry')

    user_id = str(clbk.from_user.id)
    user_data = await db1.get(user_id)
    user_data_dict = json.loads(user_data.decode('utf-8'))
    user_data_dict['income'] = {}
    user_data_dict['expenses'] = {}
    await db1.set(user_id, json.dumps(user_data_dict))
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
    user_data = await db1.get(user_id)

    if not user_data:
        await add_user_in_db(user_id)

    user_data_dict = json.loads(user_data.decode('utf-8'))

    data = await state.get_data()

    logger_db_utils.debug(f'{data=}')
    amount = data.get('amount')
    logger_db_utils.debug(f'{amount=}')

    try:
        user_data_dict['balance'] += round(amount, 2)
    except Exception as err:
        logger_db_utils.error(f'{err=}')
    try:
        user_data_dict['income'][category] = (
                user_data_dict['income'].setdefault(category, 0) + amount)
    except Exception as err:
        logger_db_utils.error(f'{err=}')
    logger_db_utils.debug('Exit')
    await db1.set(user_id, json.dumps(user_data_dict))
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
    user_data = await db1.get(user_id)
    user_data_dict = json.loads(user_data.decode('utf-8'))
    user_data_dict['balance'] -= amount
    user_data_dict['expenses'][category][subcategory] = (
            user_data_dict['expenses'].setdefault(category, {}).setdefault(
                    subcategory, 0) + amount)

    await db1.set(user_id, json.dumps(user_data_dict))
    await set_data_json()

    logger_db_utils.debug('Exit')


async def generate_fin_stats(clbk: CallbackQuery) -> str:
    date: str = clbk.message.date.strftime('%d.%m.%Y %H:%M (UTC)')
    user_id = str(clbk.from_user.id)
    logger_db_utils.debug(f'Entry\n{date=}:{user_id=}')
    user_data = await db1.get(user_id)
    user_data_dict = json.loads(user_data.decode('utf-8'))

    monthly_income = user_data_dict['income']
    sum_income = sum(monthly_income.values())
    balance: int | float = round(user_data_dict['balance'], 2)
    expenses: dict[str, dict[str, float | int]] = user_data_dict['expenses']
    sum_expenses = sum(
            sum(obj) for obj in (categ.values() for categ in expenses.values()))

    report: str = (f'<code><i>{date}</i></code>\n\n'
                   f'<b>Баланс: </b><code>{balance}</code>\n'
                   f'<b>Сальдо:</b>'
                   f' <code>{round(balance - sum_expenses, 2)}</code>\n'
                   f'<b>------------------------</b>\n'
                   f'<b>Доходы за месяц:</b> <code>{sum_income}</code>\n')

    for category, value in monthly_income.items():
        report += f'  - {INCOME_CATEG_BUTT[category]}: <code>{value}</code>\n'
    report += (f'<b>------------------------\n'
               f'Расходы за месяц:</b> <code>{round(sum_expenses, 2)}</code>\n')

    for category, data in expenses.items():
        report += f'  <b>{EXPENSES_CATEG_BUTT[category]}:</b>\n'
        for subcategory, value in data.items():
            report += (f'    - {EXPENSE_SUBCATEGORY_BUTT[subcategory]}: '
                       f'<code>{round(value, 2)}</code>'
                       f'<code>'
                       f'{await _calc_percent(sum_income, value)}</code>\n')
    logger_db_utils.debug('Exit')
    return report


async def get_users() -> set[str]:
    """
    Returns IDs users
    :return: set[str]
    """
    logger_db_utils.debug('Entry')
    users = {str(user_id.decode()) for user_id in await db1.keys()}
    logger_db_utils.debug(f'{users=}')
    logger_db_utils.debug('Exit')
    return users
