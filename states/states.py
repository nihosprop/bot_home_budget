from aiogram.fsm.state import StatesGroup, State


class FSMMakeTransaction(StatesGroup):
    fill_number = State()
    select_direction = State()
    select_income = State()
    select_expenses = State()
    select_subcategory = State()
