import asyncio
import logging

from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config_data.config import Config, load_config
from keyboards.set_menu import set_main_menu
from handlers import other_handlers, user_handlers


logger = logging.getLogger(__name__)
storage = MemoryStorage()
user_dict: dict[int, dict[str, str | int | bool]] = {}

async def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(filename)s:%(lineno)d #%(levelname)-8s '
                               '[%(asctime)s] - %(name)s - %(message)s',
                        datefmt='%Y.%m.%d %H:%M:%S')

    logger.info('Start bot')

    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

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
