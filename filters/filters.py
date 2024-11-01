from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsNumber(BaseFilter):
    def __call__(self, message: Message) -> bool:
        number = message.text.replace(',', '.')

        try:
            int(number)
        except ValueError:
            try:
                float(number)
            except ValueError:
                return False
            else:
                return True
        else:
            return True
