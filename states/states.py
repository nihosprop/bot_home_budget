import logging

from aiogram.fsm.state import StatesGroup, State

logger_states = logging.getLogger(__name__)

class FSMMakeTransaction(StatesGroup):
    fill_number = State()
    select_direction = State()
    select_income = State()
    select_expenses = State()
    select_subcategory = State()
