import logging
import math

from aiogram.enums import ContentType
from aiogram.filters import BaseFilter
from aiogram.types import Message

logger_filters = logging.getLogger(__name__)


class IsNumber(BaseFilter):
    """ Filter to check if the message content is a number. """

    async def __call__(self, msg: Message) -> bool | dict[str, int | float]:
        """ Checks whether the message content is a number. Returns
        False if the content is not a number. Returns a dictionary with
        number if the content is a number.
        """
        if msg.content_type is ContentType.TEXT:
            number = msg.text.replace(',', '.')
            user_id = msg.from_user.id
            try:
                value = {'number': int(number)}
            except ValueError:
                try:
                    if not math.isfinite(float(number)):

                        logger_filters.warning(f'NaN or INF attempt!!! ->'
                                               f' {user_id=}: {number=}')
                        return False
                    value = {'number': float(number)}
                except ValueError:
                    logger_filters.warning(
                        f'Failed to convert message to number:'
                        f' {user_id=}: {msg.text=}')
                    return False
            logger_filters.debug(f'{value=}')
            return value if value['number'] != 0 else False
        logger_filters.debug(f'drop_update -> {msg.content_type}')

        return False

class IsAdmin(BaseFilter):
    async def __call__(self, msg: Message, superadmin) -> bool:
        logger_filters.debug('Entry')
        user_id = str(msg.from_user.id)
        logger_filters.debug(f'In {__class__.__name__}:{user_id=}'
                             f':{superadmin=}\n{user_id == superadmin=}')
        logger_filters.debug('Exit')
        return user_id == superadmin
