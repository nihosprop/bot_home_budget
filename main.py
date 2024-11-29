import asyncio
import logging
import yaml

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data.config import Config, load_config
from keyboards.set_menu import set_main_menu
from handlers import other_handlers, user_handlers

logger_main = logging.getLogger(__name__)
storage = MemoryStorage()


async def main():

    with open('logs/logging_setting/logging_config.yaml', 'rt') as file:
        log_config = yaml.safe_load(file.read())
    dictConfig(log_config)

    logger_main.info('Start bot')

    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)

    # menu_button_setting
    await set_main_menu(bot)

    # registering_routers
    dp.include_router(user_handlers.user_router)
    dp.include_router(other_handlers.other_router)

    # skip_updates
    await bot.delete_webhook(drop_pending_updates=True)
    # start polling
    await dp.start_polling(bot)


asyncio.run(main())
