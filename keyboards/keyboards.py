from keyboards.keyboard_utils import create_inline_kb
from lexicon.lexicon_ru import GAIN_CATEGORIES, DIRECTION

kb_for_gain = create_inline_kb(2, **GAIN_CATEGORIES)
kb_direction = create_inline_kb(2, **DIRECTION)
