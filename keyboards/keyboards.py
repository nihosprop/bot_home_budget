from keyboards.keyboard_utils import create_inline_kb
from lexicon.lexicon_ru import INCOME_CATEGORIES, DIRECTION, EXPENSES_CATEGORIES

kb_gain_categories = create_inline_kb(2, **INCOME_CATEGORIES)
kb_expenses_categories = create_inline_kb(2, **EXPENSES_CATEGORIES)
kb_direction = create_inline_kb(2, **DIRECTION)
