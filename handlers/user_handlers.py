import logging
from aiogram import Router, F
from lexicon.lexicon_ru import LexiconRu
from aiogram.types import CallbackQuery, Message

logger = logging.getLogger(__name__)
user_router = Router()

