from aiogram import Bot
from aiogram.types import BotCommand
from lexicon.lexicon_ru import LexiconCommandsRu

lexicon_cmd_ru = LexiconCommandsRu()

async def set_main_menu(bot: Bot):
    main_menu_commands = [BotCommand(command=command, description=description)
            for command, description in lexicon_cmd_ru.__dict__.items()]
    await bot.set_my_commands(main_menu_commands)
