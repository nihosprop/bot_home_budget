from aiogram.enums import ContentType
from aiogram.filters import BaseFilter
from aiogram.types import Message
import logging

filters_logger = logging.getLogger(__name__)

class IsNumber(BaseFilter):

    async def __call__(self, message: Message) -> bool | dict[str, int | float]:

        if message.content_type is ContentType.TEXT:
            number = message.text.replace(',', '.')
            try:
                value = {'number': int(number)}
            except ValueError:
                try:
                    value = {'number': float(number)}
                except ValueError:
                    return False
            return value
        filters_logger.info(f'drop_update -> {message.content_type}')
        return False
