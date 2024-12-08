from dataclasses import dataclass
import logging

logger_lexicon = logging.getLogger(__name__)


@dataclass
class LexiconCommandsRu:
    start: str = 'Запуск'


@dataclass
class LexiconRu:
    await_start = ('<b>Что-бы запустить бота нажмите:\n'
                   '-> /start</b>')
    await_amount: str = '<b>Ожидаю ввод суммы…</b>👇'
    await_direction: str = '<b>Ожидается выбор направления…</b>'
    await_categories: str = '<b>Ожидается выбор категории…</b>'
    select_direction: str = 'Выберите направление'
    select_category: str = 'Выберите категорию'
    transaction_recorded: str = 'Транзакция записана!✅'
    text_confirm_del_data: str = 'Подтвердить удаление данных!'
    text_problems: str = 'Нажмите: <b>/start</b>'
    text_del_success_data: str = ('Ваши данные удалены!✅\n'
                                  'Нажмите <b>/start</b> что-бы начать')
    text_confirm_reset_month: str = ('Подтвердите сброс статистики за месяц.\n'
                                     'Общий баланс затронут не будет.')
    text_help: str = (f'Бот находится в постоянном ожидании суммы(числа).\n'
                      'Вам нужно:\n'
                      '1. Ввести сумму.\n'
                      '2. Выбрать одно из направлений:\n'
                      '\t-> Доходы/Расходы\n'
                      '3. Выбрать категорию для записи транзакции.\n'
                      'Что-бы посмотреть структуру категорий нажмите:\n'
                      '-> <b>/category</b>\n\n')
    text_statistics_reset: str = ('Статистика за месяц обнулена!✅\nВведите '
                                  'сумму👇')


@dataclass
class Categories:
    pass


# collect into dataclass Categories
DIRECTION_BUTT: dict[str, str] = {'income': 'Доходы', 'expenses': 'Расходы'}

INCOME_CATEG_BUTT: dict[str, str] = {
        'salary': 'Зарплата',
        'other': 'Иное',
        'prepayment': 'Аванс',
        'present': 'Подарки',
        'dividends': 'Дивиденды',
        'temporary_work': 'Подработка'}

EXPENSES_CATEG_BUTT: dict[str, str] = {
        'supermarket': 'Супермаркет',
        'feeding': 'Питание',
        'transport': 'Транспорт',
        'utility_payments': 'Коммуналка',
        'entertainment_and_relaxation': 'Развлечения и отдых',
        'health_and_beauty': 'Здоровье и красота',
        'education': 'Образование',
        'clothing_and_accessories': 'Одежда и аксессуары',
        'pets': 'Домашние животные',
        'misc_expenses': 'Прочие расходы',
        'household_expenses': 'Бытовые расходы',
        'debts': 'Задолженности'}

SUPERMARKET_BUTT = {'products': 'Продукты', 'alcohol': 'Алкоголь'}
FEEDING_BUTT = {'restaurant': 'Ресторан', 'cafe': 'Кафе', 'canteen': 'Столовая'}
TRANSPORT_BUTT = {'personal': 'Личный', 'public': 'Общественный'}
UTILITIES_BUTT = {
        'rent': 'Квартплата',
        'electricity': 'Электричество',
        'internet': 'Интернет',
        'mobile': 'Моб связь',
        'housing_rent': 'Аренда жилья',
        'repair_maintenance': 'Обслуживание и ремонт'}
ENTERTAINMENT_BUTT = {
        'cinema_theater': 'Кино и театр',
        'hobbies': 'Хобби',
        'flights': 'Авиабилеты',
        'car_rental': 'Аренда авто',
        'travel_packages': 'Путевки'}
HEALTH_BEAUTY_BUTT = {
        'medical_services': 'Мед услуги',
        'fitness': 'Фитнес',
        'self_care': 'Уход за собой'}
EDUCATION_BUTT = {
        'courses_training': 'Курсы и обучение',
        'books_materials': 'Книги и материалы',
        'child_education': 'Детское образование'}
CLOTHING_ACCESSORIES_BUTT = {'clothing': 'Одежда', 'accessories': 'Аксессуары'}
PETS_BUTT = {
        'food': 'Корм',
        'medical_expenses': 'Медицинские расходы',
        'accessories_toys': 'Аксессуары и игрушки',
        'grooming': 'Груминг'}
MISC_EXPENSES_BUTT = {
        'gifts': 'Подарки',
        'donations': 'Пожертвования',
        'investing': 'Инвестинг'}
HOUSEHOLD_NEEDS_BUTT = {
        'dry_cleaning': 'Химчистка',
        'home_goods': 'Товары для дома',
        'household_chemicals': 'Бытовая химия',
        'electronics': 'Техника и электроника',
        'plumbing': 'Сантехника'}
DEBTS_BUTT = {
        'loan': 'Кредит',
        'installment': 'Рассрочка',
        'mortgage': 'Ипотека',
        'borrowing': 'Займ'}

EXPENSE_SUBCATEGORY_BUTT: dict[str, str] = dict(**SUPERMARKET_BUTT,
                                                **FEEDING_BUTT, **TRANSPORT_BUTT,
                                                **DEBTS_BUTT,
                                                **HOUSEHOLD_NEEDS_BUTT,
                                                **MISC_EXPENSES_BUTT,
                                                **PETS_BUTT,
                                                **CLOTHING_ACCESSORIES_BUTT,
                                                **EDUCATION_BUTT,
                                                **HEALTH_BEAUTY_BUTT,
                                                **ENTERTAINMENT_BUTT,
                                                **UTILITIES_BUTT)

CANCEL_BUTT: dict[str, str] = {'cancel': '❌ОТМЕНА'}
YES_NO_BUTT: dict[str, str] = {'yes': '🗑️Удалить', '/cancel': '❌Отмена'}
RESET_CANCEL_BUTT: dict[str, str] = {'/reset': 'Сброс', '/cancel': '❌Отмена'}
FOR_AWAIT_AMOUNT_BUTT: dict[str, str] = {
        'reset_month_stats': 'Сброс статистики за месяц',
        'delete_user_data': 'Стереть все данные',
        '/category': 'Категории',
        '/report': 'Отчет'}
MAP = """
Доходы:
  1.Зарплата
  2.Аванс
  3.Иное
  4.Подработка
  5.Подарки 
  6.Инвестиции

Расходы:
  1.Супермаркет
    — Продукты
    — Алкоголь
  2.Питание
    — Ресторан
    — Кафе
    — Столовая
  3.Транспорт
    — Личный
    — Общественный
  4.Коммуналка
    — Квартплата
    — Электричество
    — Интернет
    — Моб связь
    — Аренда жилья
    — Обслуживание и ремонт
  5.Развлечения и Отдых
    — Кино и театр
    — Хобби
    — Авиабилеты
    — Аренда авто
    — Путевки
  6.Здоровье и красота
    — Мед услуги
    — Фитнес
    — Уход за собой
  7.Образование
    — Курсы и обучение
    — Книги и материалы
    — Детское образование
  8.Одежда и аксессуары
    — Одежда
    — Аксессуары
  9.Домашние животные
    — Корм
    — Медицинские расходы
    — Аксессуары и игрушки
    — Груминг
  10.Прочие расходы
    — Подарки
    — Пожертвования
    — Инвестинг
  11.Бытовые нужды
    — Химчистка
    — Товары для дома
    — Бытовая химия
    — Техника и электроника
    — Сантехника
  12.Долги 
    — Кредит
    — Рассрочка
    — Ипотека 
    — Займ
"""
