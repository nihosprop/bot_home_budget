import logging
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from database.db import database as db

logger_utils = logging.getLogger(__name__)

async def add_income_in_db(clbk: CallbackQuery,
                           state: FSMContext):
    category = clbk.data
    user_id = str(clbk.from_user.id)
    data = await state.get_data()
    amount = data['amount']
    db.setdefault(user_id, {'income': {}, 'expenses': {}})
    db[user_id]['income'][category] = (
            db[user_id]['income'].setdefault(category, 0) + amount)

async def add_expenses_in_db(clbk: CallbackQuery,
                           state: FSMContext):
    category = clbk.data
    user_id = str(clbk.from_user.id)
    data = await state.get_data()
    amount = data['amount']
    db.setdefault(user_id, {'income': {}, 'expenses': {}})
    db[user_id]['expenses'][category] = (
            db[user_id]['expenses'].setdefault(category, 0) + amount)
