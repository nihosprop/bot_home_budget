import logging

from aiogram import Bot
from aiogram.types import BotCommand
from lexicon.lexicon_ru import LexiconCommandsRu

logger_set_menu = logging.getLogger(__name__)

async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(command=command, description=description)
            for command, description in LexiconCommandsRu().__dict__.items()]
    await bot.set_my_commands(main_menu_commands)
