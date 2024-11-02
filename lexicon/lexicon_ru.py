from dataclasses import dataclass


@dataclass
class LexiconCommandsRu:
    start: str = 'Начало'
    help: str = 'Справка'


@dataclass
class LexiconRu:
    start: str = ('Это бот учета личных финансов.\nОтправьте сумму(целое или '
                  'вещественное число) и выберите '
                  'категорию.')
    help: str = 'Это команда /help'
    other_message: str = 'Пришлите целое или вещественное число!'
    select_direction: str = 'Выберите направление'
    select_category: str = 'Выберите категорию'
    transaction_recorded: str = 'Транзакция записана!'
    waiting_number: str = 'В ожидании суммы..'


DIRECTION: dict[str, str] = {
        'gain': 'Доходы',
        'expenses': 'Расходы'}

GAIN_CATEGORIES: dict[str, str] = {
        'salary': 'Зарплата',
        'prepayment': 'Аванс',
        'other': 'Иное'}

BUTTONS: dict[str, str] = {
        'cancel': 'Отмена'}
