import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from filters.filters import IsAdmin
from keyboards.keyboards import kb_admin, kb_back, kb_for_wait_amount, kb_game
from lexicon.lexicon_ru import LexiconRu
from states.states import FSMAdminPanel
from utils.utils import MessageProcessor

admin_router = Router()
admin_router.message.filter(IsAdmin())

logger_admin = logging.getLogger(__name__)


@admin_router.message(F.text == '/admin')
async def cmd_admin(msg: Message, state: FSMContext):
    await msg.delete()
    await msg.answer('<code>💻 Админ панель 💻</code>', reply_markup=kb_admin)
    await state.set_state(FSMAdminPanel.admin_menu)

@admin_router.message(F.text == '/reboot')
async def cmd_reboot(msg: Message, state: FSMContext):
    logger_admin.debug(f'Entry')

    await msg.answer(LexiconRu.await_amount, reply_markup=kb_for_wait_amount)
    await state.set_state(state=None)

    logger_admin.debug(f'Exit')

@admin_router.callback_query(F.data == 'temp')
async def clbk_temp(clbk: CallbackQuery, state: FSMContext):
    # await clbk.message.edit_text('Слово дня загадано!\n'
    #                              'Попробуй угадать:\n➖  ➖  ➖  ➖  ➖ \n'
    #                              'ПОПЫТКИ ❤️❤️❤️❤️❤️❤️', reply_markup=kb_game)
    await flush_redis_db()

@admin_router.callback_query(F.data == 'exit')
async def cmd_exit(clbk: CallbackQuery, state: FSMContext):
    await state.set_state(state=None)
    await clbk.message.edit_text(f'Вы вышли из админ-панели✅',
                                 reply_markup=kb_for_wait_amount)
    await clbk.answer()


@admin_router.message(FSMAdminPanel.admin_menu)
async def invalid_msg(msg: Message):
    await msg.delete()


@admin_router.callback_query(F.data == 'newsletter', FSMAdminPanel.admin_menu)
async def cmd_newsletter(clbk: CallbackQuery, state: FSMContext):
    await clbk.message.edit_text('Введите текст рассылки.\nПоcле отправки '
                                 'текста боту, начнется рассылка '
                                 'пользователям!', reply_markup=kb_back)
    await state.set_state(FSMAdminPanel.newsletter)
    await clbk.answer()


@admin_router.callback_query(F.data == 'back', FSMAdminPanel.newsletter)
async def clbk_back(clbk: CallbackQuery, state: FSMContext):
    await clbk.message.edit_text('<code>Админ-панель</code>',
                                 reply_markup=kb_admin)
    await state.set_state(FSMAdminPanel.admin_menu)


@admin_router.message(FSMAdminPanel.newsletter)
async def sent_text(msg: Message, state: FSMContext):
    await MessageProcessor(msg, state).broadcast(text=msg.text)
    await msg.answer('Рассылка произведена✅', reply_markup=kb_admin)
    await state.set_state(FSMAdminPanel.admin_menu)
