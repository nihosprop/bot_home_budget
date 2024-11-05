from keyboards.keyboard_utils import create_inline_kb
from lexicon.lexicon_ru import GAIN_CATEGORIES, DIRECTION

kb_gain_categories = create_inline_kb(2, **GAIN_CATEGORIES)
kb_direction = create_inline_kb(2, **DIRECTION)
