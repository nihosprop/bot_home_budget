import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import CallbackQuery, Message, TelegramObject, User

from lexicon.lexicon_ru import LexiconRu

logger_middl_outer = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseMiddleware):
    """A middleware for limiting the frequency of requests from a single user.
    Uses Redis to store information about request frequency. If the frequency
    exceeds the set threshold, requests are blocked.
    Attributes:
        storage (RedisStorage): An object for interacting with Redis.
        ttl (int | None): The time-to-live for the key in milliseconds. If
        None, rate limiting is disabled. """

    def __init__(self, storage: RedisStorage, ttl: int | None = None):
        """
        Initializes the middleware for limiting the frequency of requests.
        Args: storage (RedisStorage): An object for interacting with Redis.
        ttl (int | None, optional): The time-to-live for the key in
        milliseconds. If None, rate limiting is disabled.
        :param storage:
        :param ttl:
        """
        self.storage = storage
        self.ttl = ttl

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject, data: Dict[str, Any]) -> Any:
        """Handles an event and applies the frequency limitation. If rate
        limiting is enabled and the user has exceeded the allowed frequency,
        the event is ignored and the user receives an appropriate
        notification. Args: handler (Callable): The next handler in the chain.
        event (TelegramObject): The current event. data (Dict[str, Any]):
        Additional data. Returns: Any: The result of calling the next handler.
        """
        logger_middl_outer.debug(f'Entry {__class__.__name__}')

        if self.ttl is None:
            return await handler(event, data)

        user: User = data.get('event_from_user')
        throttl_user_id = f'throttl_{user.id}'
        check_user = await self.storage.redis.get(name=throttl_user_id)
        logger_middl_outer.debug(f'{check_user=}')

        if check_user and int(check_user.decode()) == 1:
            if isinstance(event, Message):
                await event.answer(text=LexiconRu.text_antispam)
            if isinstance(event, CallbackQuery):
                await event.answer()

            logger_middl_outer.warning(f'Throttling:{throttl_user_id=}')
            return None

        await self.storage.redis.set(name=throttl_user_id, value=1, px=self.ttl)
        logger_middl_outer.debug(f'Exit {__class__.__name__}')
        return await handler(event, data)
