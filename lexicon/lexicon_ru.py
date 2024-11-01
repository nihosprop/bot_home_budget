from dataclasses import dataclass


@dataclass
class LexiconCommandsRu:
    start: str = 'Начало'
    help: str = 'Справка'


@dataclass
class LexiconRu:
    start: str = 'Это команда /start'
    help: str = 'Это команда /help'
    other_message: str = 'Пришлите целое или вещественное число!'
    select_categories: str = 'Выберите категорию'


LEXICON: dict[str, str] = {'gain': 'Доходы', 'expenses': 'Расходы'}
