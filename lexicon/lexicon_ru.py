from dataclasses import dataclass

LEXICON_COMMANDS_RU: dict[str, str] = {
        '/start': 'Начало',
        '/help': 'Справка'}

@dataclass
class LexiconRu:
    other_message: str = 'пишите по делу!'
