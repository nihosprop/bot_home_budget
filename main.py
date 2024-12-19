import asyncio
import logging
from logging.config import dictConfig

import yaml
from aiogram.fsm.storage.redis import Redis, RedisStorage
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config_data.config import Config, load_config
from keyboards.set_menu import set_main_menu
from handlers import other_handlers, user_handlers
from database.db_utils import db1, get_data_json
from middlewares.outer import ThrottlingMiddleware

logger_main = logging.getLogger(__name__)


async def main():
    with open('logs/logging_setting/logging_config.yaml', 'rt') as file:
        log_config = yaml.safe_load(file.read())
    dictConfig(log_config)
    logger_main.info('Loading logging settings success')

    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    redis = Redis(host='localhost', port=6379, db=0)

    try:
        await redis.ping()
        logger_main.info("Redis connection established successfully.")
    except Exception as e:
        logger_main.error(f"Error connecting to Redis: {e}")
        raise

    storage = RedisStorage(redis=redis)
    dp = Dispatcher(storage=storage)

    # throttling storage
    storage_throttling: RedisStorage = RedisStorage.from_url(
            'redis://localhost:6379/7')

    try:
        await get_data_json()
        logger_main.info('Loading from a db.json success')

        await set_main_menu(bot)

        # routers
        dp.include_router(user_handlers.user_router)
        dp.include_router(other_handlers.other_router)

        # middlewares
        dp.message.outer_middleware(
                ThrottlingMiddleware(storage=storage_throttling, ttl=700))
        dp.callback_query.outer_middleware(
                ThrottlingMiddleware(storage=storage_throttling, ttl=500))

        await bot.delete_webhook(drop_pending_updates=True)
        logger_main.info('Start bot')
        await dp.start_polling(bot)
    except Exception as err:
        logger_main.exception(err)
        raise

    finally:
        await redis.aclose()
        await db1.aclose()
        await storage_throttling.redis.aclose()
        logger_main.info('Stop bot')


if __name__ == "__main__":
    asyncio.run(main())
