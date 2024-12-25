from dataclasses import dataclass
from environs import Env

@dataclass
class TgBot:
    token: str
    id_admin: str

@dataclass
class Config:
    tg_bot: TgBot

def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(tg_bot=TgBot(token=env('BOT_TOKEN'), id_admin=env('ID_ADMIN')))
