from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsNumber(BaseFilter):

    async def __call__(self, message: Message) -> bool | dict[str, int | float]:
        number = message.text.replace(',', '.')
        try:
            value = {'number': int(number)}
        except ValueError:
            try:
                value = {'number': float(number)}
            except ValueError:
                return False
        return value
