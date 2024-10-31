import logging

from aiogram.types import Message
from aiogram import Router

logger = logging.getLogger(__name__)
other_router = Router()

@other_router.message()
async def answer_to_another(message: Message):
    user_name = message.from_user.username or message.from_user.first_name
    await message.answer(f'{user_name}пишите по делу!')

