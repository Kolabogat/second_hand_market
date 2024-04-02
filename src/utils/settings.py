from environs import Env
from dataclasses import dataclass


# ENVIRONMENTS
@dataclass
class SuperBot:
    bot_token: str
    ADMIN_ID: int


@dataclass
class PostgreSQL:
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: int
    POSTGRES_PORT: int
    POSTGRES_DB: str


@dataclass
class Redis:
    REDIS_HOST: str
    REDIS_PASSWORD: str
    REDIS_PORT: int


@dataclass
class Settings:
    super_bot: SuperBot
    postgresql: PostgreSQL
    redis: Redis


def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        super_bot=SuperBot(
            bot_token=env.str('TOKEN'),
            ADMIN_ID=env.int('ADMIN_ID')
        ),
        postgresql=PostgreSQL(
            POSTGRES_HOST=env.str('POSTGRES_HOST'),
            POSTGRES_PORT=env.int('POSTGRES_PORT'),
            POSTGRES_USER=env.str('POSTGRES_USER'),
            POSTGRES_PASSWORD=env.str('POSTGRES_PASSWORD'),
            POSTGRES_DB=env.str('POSTGRES_DB'),
        ),
        redis=Redis(
            REDIS_HOST=env.str('REDIS_HOST'),
            REDIS_PASSWORD=env.str('REDIS_PASSWORD'),
            REDIS_PORT=env.int('REDIS_PORT'),
        )
    )


settings = get_settings('.env')
