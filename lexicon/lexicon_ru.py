from dataclasses import dataclass


@dataclass
class LexiconCommandsRu:
    start: str = 'Начало'
    help: str = '/help'


@dataclass
class LexiconRu:
    help: str = 'Это команда /help'
    other_message: str = 'Пишите по делу!'
