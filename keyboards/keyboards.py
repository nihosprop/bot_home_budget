import logging
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
                                DEBTS_BUTT,
                                CLOTHING_ACCESSORIES_BUTT,
                                YES_NO_BUTT)

logger_keyboards = logging.getLogger(__name__)

kb_yes_cancel = create_inline_kb(2, cancel_butt=False, **YES_NO_BUTT)

kb_direction = create_inline_kb(2, **DIRECTION_BUTT)
kb_income_categories = create_inline_kb(3, **INCOME_CATEG_BUTT)
kb_expenses_categories = create_inline_kb(2, **EXPENSES_CATEG_BUTT)

kb_supermarket = create_inline_kb(2, **SUPERMARKET_BUTT)
kb_feeding = create_inline_kb(2, **FEEDING_BUTT)
kb_transport = create_inline_kb(2, **TRANSPORT_BUTT)
kb_utility_payments = create_inline_kb(2, **UTILITIES_BUTT)
kb_entertainment = create_inline_kb(2, **ENTERTAINMENT_BUTT)
kb_health = create_inline_kb(2, **HEALTH_BEAUTY_BUTT)
kb_education = create_inline_kb(2, **EDUCATION_BUTT)
kb_pets = create_inline_kb(2, **PETS_BUTT)
kb_misc = create_inline_kb(2, **MISC_EXPENSES_BUTT)
kb_household = create_inline_kb(2, **HOUSEHOLD_NEEDS_BUTT)
kb_debts = create_inline_kb(2, **DEBTS_BUTT)
kb_clothing = create_inline_kb(2, **CLOTHING_ACCESSORIES_BUTT)

kbs_for_expenses: dict[str, InlineKeyboardMarkup] = {
        'supermarket': kb_supermarket,
        'feeding': kb_feeding,
        'transport': kb_transport,
        'utility_payments': kb_utility_payments,
        'entertainment_and_relaxation': kb_entertainment,
        'health_and_beauty': kb_health,
        'education': kb_education,
        'pets': kb_pets,
        'misc_expenses': kb_misc,
        'household_expenses': kb_household,
        'clothing_and_accessories': kb_clothing,
        'debts': kb_debts}
