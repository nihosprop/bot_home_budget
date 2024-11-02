from aiogram.fsm.state import StatesGroup, State


class FSMMakeTransaction(StatesGroup):
    fill_number = State()
    select_direction = State()
    select_category = State()
    select_subcategory = State()
