import logging
import math

from aiogram.enums import ContentType
from aiogram.filters import BaseFilter
from aiogram.types import Message

logger_filters = logging.getLogger(__name__)

class IsNumber(BaseFilter):
    """ Filter to check if the message content is a number. """

    async def __call__(self, message: Message) -> bool | dict[str, int | float]:
        """ Checks whether the message content is a number. Returns
        False if the content is not a number. Returns a dictionary with
        number if the content is a number.
        """
        if message.content_type is ContentType.TEXT:
            number = message.text.replace(',', '.')
            try:
                value = {'number': int(number)}
            except ValueError:
                try:
                    if not math.isfinite(float(number)):
                        user_id = message.from_user.id
                        logger_filters.error(f'NaN or INF attempt!!! ->'
                                             f' {user_id=}')
                        return False

                    value = {'number': float(number)}
                except ValueError:
                    logger_filters.info(f'Failed to convert message to number:'
                                        f' {message.text}')
                    return False
            logger_filters.debug(f'{value=}')
            return value if value['number'] != 0 else False
        logger_filters.debug(f'drop_update -> {message.content_type}')

        return False
