import asyncio
import logging
from logging.config import dictConfig

import yaml

from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data.config import Config, load_config
from keyboards.set_menu import set_main_menu
from handlers import other_handlers, user_handlers
from database.db_utils import get_data_json, db1

logger_main = logging.getLogger(__name__)

async def check_redis_connection(redis):
    try:
        await redis.ping()
        logger_main.info("Redis connection established successfully.")
    except Exception as e:
        logger_main.error(f"Error connecting to Redis: {e}")
        raise


async def main():
    with open('logs/logging_setting/logging_config.yaml', 'rt') as file:
        log_config = yaml.safe_load(file.read())
    dictConfig(log_config)
    logger_main.info('Loading logging settings success')

    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    redis = Redis(host='localhost', port=6379, db=0)
    await check_redis_connection(redis)
    storage = RedisStorage(redis=redis)

    dp = Dispatcher(storage=storage)

    try:
        await get_data_json()
        logger_main.info('Loading from a db.json success')

        await set_main_menu(bot)

        dp.include_router(user_handlers.user_router)
        dp.include_router(other_handlers.other_router)

        await bot.delete_webhook(drop_pending_updates=True)
        logger_main.info('Start bot')
        await dp.start_polling(bot)
    except Exception as err:
        logger_main.exception(err)
        raise

    finally:
        logger_main.info('Stop bot')
        await db1.aclose()


if __name__ == "__main__":
    asyncio.run(main())
