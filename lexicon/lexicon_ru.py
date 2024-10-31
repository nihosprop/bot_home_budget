from dataclasses import dataclass


@dataclass
class LexiconCommandsRu:
    start: str = 'Начало',
    help: str = 'Справка'


@dataclass
class LexiconRu:
    other_message: str = 'пишите по делу!'
