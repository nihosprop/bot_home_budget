from dataclasses import dataclass


@dataclass
class LexiconCommandsRu:
    start: str = 'Начало'
    help: str = 'Справка'
    category: str = 'Посмотреть категории'


@dataclass
class LexiconRu:
    start: str = ('Это бот учета личных финансов.\n'
                  'Отправьте сумму(целое или вещественное число) и выберите '
                  'категорию.')
    help: str = 'Это команда /help'
    other_message: str = 'Пришлите целое или вещественное число!'
    select_direction: str = 'Выберите направление'
    select_category: str = 'Выберите категорию'
    select_subcategory: str = 'Выберите под-категорию'
    transaction_recorded: str = 'Транзакция записана!'
    waiting_number: str = 'В ожидании суммы..'


# collect_into_dataclass
DIRECTION: dict[str, str] = {
        'gain': 'Доходы',
        'expenses': 'Расходы'}

GAIN_CATEGORIES: dict[str, str] = {
        'salary': 'Зарплата',
        'other': 'Иное',
        'prepayment': 'Аванс',
        'present': 'Подарки',
        'investments': 'Инвестиции',
        'temporary_work': 'Подработка'}

EXPENSES_CATEGORIES: dict[str, str] = {
        'products': 'Продукты',
        'feeding': 'Питание',
        'transport': 'Транспорт',
        'utility_payments': 'Коммунальные платежи',
        'entertainment_and_relaxation': 'Развлечения и отдых',
        'health_and_beauty': 'Здоровье и красота',
        'education': 'Образование',
        'clothing_and_accessories': 'Одежда и аксессуары',
        'pets': 'Домашние животные',
        'other_expenses': 'Прочие расходы',
        'household_expenses': 'Бытовые расходы',
        'arrears': 'Задолженности'}

PRODUCTS = {
        'supermarket': 'Супермаркет',
        'alcohol': 'Алкоголь'}
FEEDING = {
        'restaurant': 'Ресторан',
        'cafe': 'Кафе',
        'canteen': 'Столовая'}

BUTTONS: dict[str, str] = {
        'cancel': '❌Отмена'}

MAP = """
Доходы:
1. Зарплата
2. Аванс 
3. Иное
4. Подработка
5. Подарки 
6. Инвестиции

Расходы
1. Продукты
    — Супермаркет
    — Алкоголь
2. Питание
    — Ресторан
    — Кафе
    — Столовая
3. Транспорт
    — Личный
        — Топливо
        — Ремонт и обслуживание
    — Общественный
        — Автобус
        — Метро
        — Такси
        — Трамвай
        — Поезд
4. Коммунальные платежи
    — Квартплата
    — Электричество
    — Интернет
    — Моб связь
    — Аренда жилья
    — Обслуживание и ремонт
5. Развлечения и Отдых
    — Кино и театр
    — Хобби
    — Авиабилеты
    — Аренда авто
    — Путевки
6. Здоровье и красота
    — Мед услуги
    — Фитнес
    — Уход за собой
7. Образование
    — Курсы и обучение
    — Книги и материалы
    — Детское образование
8. Одежда и аксессуары
    — Одежда
    — Обувь
    — Аксессуары
9. Домашние животные
    — Корм
    — Медицинские расходы
    — Аксессуары и игрушки
    — Груминг
10. Прочие расходы
    — Подарки
    — Пожертвования
    — Инвестинг
11. Бытовые нужды
    — Химчистка
    — Товары для дома.
    — Бытовая химия
    — Техника и электроника
    — Сантехника
12. Долги 
    — Кредит
    — Рассрочка
    — Ипотека 
    — Займ
"""

user_dict_example = {
        'user_id': {
                'gain': {
                        'salary': 0,
                        'prepayment': 0,
                        'temporary_work': 0,
                        'present': 0,
                        'investments': 0},
                'expenses': {
                        'food_and_drink': 0,
                        'utility_payments': 0,
                        'transport': 0}}}
