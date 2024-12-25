import logging

from aiogram import Router, F
from aiogram.types import Message

from filters.filters import IsAdmin
from keyboards.keyboards import kb_admin

admin_router = Router()
admin_router.message.filter(IsAdmin())

logger_admin = logging.getLogger(__name__)


admin_router.message(F.text == '/admin')
async def cmd_admin(msg: Message):

    await msg.answer('Админ панель', reply_markup=kb_admin)
