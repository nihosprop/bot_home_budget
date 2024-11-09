from dataclasses import dataclass


@dataclass
class LexiconCommandsRu:
    start: str = 'Начало'
    help: str = 'Справка'
    category: str = 'Посмотреть категории'


@dataclass
class LexiconRu:
    start: str = ('Это бот учета личных финансов.\n'
                  'Отправьте сумму(целое или вещественное число) и выберите'
                  ' категорию.')
    await_start = '<b>Что-бы запустить бота нажмите\n/start</b>'
    await_amount = '<b>Сейчас ожидается сумма…</b>'
    await_direction = '<b>Сейчас ожидается выбор направления…</b>'
    await_categories = '<b>Сейчас ожидается выбор категории…</b>'

    other_message: str = ('Пришлите целое или вещественное число,'
                          ' отличное от нуля!')
    select_direction: str = 'Выберите направление'
    select_category: str = 'Выберите категорию'
    select_subcategory: str = 'Выберите под-категорию'
    transaction_recorded: str = 'Транзакция записана!'
    waiting_number: str = 'Ожидаю ввод суммы…'
    problems: str = ('Что-то пошло не так\n'
                     'Нажмите: /start')
    help: str = (f'Бот находится в постоянном ожидании суммы(числа).\n'
                 'Вам нужно:\n'
                 '1. Ввести сумму.\n'
                 '2. Выбрать одно из направлений:\n'
                 '\t-> Доходы/Расходы\n'
                 '3. Выбрать категорию для записи транзакции.\n\n')

    help_default_state: str = help + await_start
    help_state_fill_number: str = help + await_amount
    help_state_direction: str = help + await_direction
    help_state_categories: str = help + await_categories


@dataclass
class Categories:
    pass


# collect into dataclass Categories
DIRECTION: dict[str, str] = {'income': 'Доходы', 'expenses': 'Расходы'}

INCOME_CATEGORIES: dict[str, str] = {
        'salary': 'Зарплата',
        'other': 'Иное',
        'prepayment': 'Аванс',
        'present': 'Подарки',
        'dividends': 'Дивиденды',
        'temporary_work': 'Подработка'}

EXPENSES_CATEGORIES: dict[str, str] = {
        'supermarket': 'Супермаркет',
        'feeding': 'Питание',
        'transport': 'Транспорт',
        'utility_payments': 'Коммуналка',
        'entertainment_and_relaxation': 'Развлечения и отдых',
        'health_and_beauty': 'Здоровье и красота',
        'education': 'Образование',
        'clothing_and_accessories': 'Одежда и аксессуары',
        'pets': 'Домашние животные',
        'other_expenses': 'Прочие расходы',
        'household_expenses': 'Бытовые расходы',
        'arrears': 'Задолженности'}

PRODUCTS = {'products': 'Продукты', 'alcohol': 'Алкоголь'}
FEEDING = {'restaurant': 'Ресторан', 'cafe': 'Кафе', 'canteen': 'Столовая'}

BUTTONS: dict[str, str] = {'cancel': '❌ОТМЕНА'}

MAP = """
Доходы:
1. Зарплата
2. Аванс 
3. Иное
4. Подработка
5. Подарки 
6. Инвестиции

Расходы
1. Супермаркет
    — Продукты
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

4. Коммуналка
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
    — Товары для дома
    — Бытовая химия
    — Техника и электроника
    — Сантехника

12. Долги 
    — Кредит
    — Рассрочка
    — Ипотека 
    — Займ
"""
