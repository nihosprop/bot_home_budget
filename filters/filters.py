from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsNumber(BaseFilter):

    async def __call__(self, message: Message) -> bool | dict[str, int | float]:
        number = message.text.replace(',', '.')

        try:
            value = int(number)
        except ValueError:
            try:
                value = float(number)
            except ValueError:
                return False
            else:
                return {'number': value}
        else:
            return {'number': value}
