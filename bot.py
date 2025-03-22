import asyncio
import logging
import betterlogging as bl

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, BotCommandScopeDefault

from tgbot.config import load_config, Config
from tgbot.handlers import routers
from tgbot.keyboards import reply
from tgbot.middlewares import ConfigMiddleware, DataBaseMiddleware, BotMiddleware
from tgbot.services import broadcaster
from tgbot.services.database import DataBase


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='🔰Головне меню'),
        BotCommand(command='add', description='💳Додати нову картку/гаманець'),
        BotCommand(command='edit', description='📝Редагувати картки/гаманці'),
        BotCommand(command='check', description='🗂Переглянути мої картки/гаманці'),
        # BotCommand(command='how_to_use', description='🗂Переглянути мої картки/гаманці'),
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


def setup_logging():
    log_level = logging.INFO
    bl.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger = logging.getLogger(__name__)
    logger.info('Starting bot')


async def on_startup(bot: Bot, admin_ids: list[int]):
    await broadcaster.broadcast(bot, admin_ids, 'Бот був запущений', reply.keyboard_home)


def register_global_middlewares(dp: Dispatcher, config: Config, database: DataBase, bot: Bot):
    dp.message.outer_middleware(ConfigMiddleware(config))
    dp.callback_query.outer_middleware(ConfigMiddleware(config))
    dp.update.middleware.register(DataBaseMiddleware(database))
    dp.update.middleware.register(BotMiddleware(bot))


async def main():
    setup_logging()
    
    config = load_config('.env')
    database = DataBase(
        host=config.db.host, user=config.db.user, password=config.db.password, name_database=config.db.database
    )

    storage = MemoryStorage()
    default = DefaultBotProperties(parse_mode='HTML')
    bot = Bot(token=config.tg_bot.token, default=default)
    dp = Dispatcher(storage=storage)

    for router in routers:
        dp.include_router(router)

    register_global_middlewares(dp, config, database, bot)

    await set_commands(bot)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error('Бот був вимкнений!')
