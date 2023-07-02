import logging
from aiogram import Bot, Dispatcher
from aiogram.utils.executor import Executor
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.logging import LoggingMiddleware

try:
    from . import config
except ImportError:
    import config


if config.DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(filename=config.LOGGING_FILE, level=logging.INFO)
logger = logging.getLogger()

# REDIS STORAGE
storage = RedisStorage2(config.REDIS_ADDRESS,
                        config.REDIS_PORT,
                        db=5,
                        pool_size=10)

bot = Bot(token=config.TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
dp.middleware.setup(LoggingMiddleware())
executor = Executor(dp, skip_updates=config.SKIP_UPDATES)
