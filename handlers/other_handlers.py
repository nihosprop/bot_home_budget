import logging

from states.states import FSMMakeTransaction
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram import Router
from lexicon.lexicon_ru import LexiconRu


logger = logging.getLogger(__name__)
other_router = Router()

