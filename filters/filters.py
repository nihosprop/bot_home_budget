from aiogram.enums import ContentType
from aiogram.filters import BaseFilter
from aiogram.types import Message
import logging

logger_filters = logging.getLogger(__name__)

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
                    logger_filters.info(f'Не удалось преобразовать сообщение в '
                                     f'число: {message.text}')
                    return False
            logger_filters.debug(f'{value=}')
            return value if value['number'] != 0 else False
        logger_filters.debug(f'drop_update -> {message.content_type}')

        return False
