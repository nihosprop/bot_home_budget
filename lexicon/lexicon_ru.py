from dataclasses import dataclass


@dataclass
class LexiconCommandsRu:
    start: str = 'Начало'
    help: str = 'Справка'


@dataclass
class LexiconRu:
    start: str = ('Это бот учета личных финансов.\nВведите сумму(целое или '
                  'вещественное число) и выберите '
                  'категорию.')
    help: str = 'Это команда /help'
    other_message: str = 'Пришлите целое или вещественное число!'
    select_categories: str = 'Выберите категорию'
    transaction_recorded: str = 'Транзакция записана!'


CATEGORY_1: dict[str, str] = {
        'gain': 'Доходы',
        'expenses': 'Расходы'}

BUTTONS: dict[str, str] = {'cancel': 'Отмена'}
