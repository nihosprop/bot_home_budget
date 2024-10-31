from dataclasses import dataclass


@dataclass
class LexiconCommandsRu:
    start: str = 'Начало'
    help: str = 'Это команда /help.\nСправка'


@dataclass
class LexiconRu:
    other_message: str = 'пишите по делу!'
