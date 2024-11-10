from aiogram.types import InlineKeyboardMarkup

from keyboards.keyboard_utils import create_inline_kb
from lexicon.lexicon_ru import (DIRECTION_BUTT,
                                EXPENSES_CATEG_BUTT,
                                INCOME_CATEG_BUTT,
                                SUPERMARKET_BUTT,
                                FEEDING_BUTT,
                                TRANSPORT_BUTT,
                                UTILITIES_BUTT,
                                ENTERTAINMENT_BUTT,
                                HEALTH_BEAUTY_BUTT,
                                EDUCATION_BUTT,
                                PETS_BUTT,
                                MISC_EXPENSES_BUTT,
                                HOUSEHOLD_NEEDS_BUTT,
                                DEBTS_BUTT)

kb_income_categories = create_inline_kb(3, **INCOME_CATEG_BUTT)
kb_direction = create_inline_kb(2, **DIRECTION_BUTT)
kb_expenses_categories = create_inline_kb(2, **EXPENSES_CATEG_BUTT)

kb_income_categories = create_inline_kb(3, **INCOME_CATEGORIES)
kb_direction = create_inline_kb(2, **DIRECTION)
kb_expenses_categories = create_inline_kb(2, **EXPENSES_CATEGORIES)
