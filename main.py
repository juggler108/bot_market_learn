import asyncio
import logging
import psycopg_pool
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from bot_market_learn.core.handlers.steps import get_name, get_date
from bot_market_learn.core.middlewares.db_middleware import DbSession
from bot_market_learn.core.others.db_entry import database_entry
from bot_market_learn.core.others.state_user import States
from bot_market_learn.core.settings import settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def start_bot(bot: Bot):
    await bot.send_message(chat_id=settings.bots.admin_id, text='Started')


async def stop_bot(bot: Bot):
    await bot.send_message(chat_id=settings.bots.admin_id, text='Stopped')


def create_pool(user, host, password, database):
    return psycopg_pool.AsyncConnectionPool(
        f"host={host} port=5432 dbname={database} user={user} password={password} connect_timeout=10")


async def run_bot():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(settings.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.middleware(DbSession(create_pool(settings.db.user, settings.db.host,
                                                settings.db.password, settings.db.db)))

    dp.message.register(get_date, States.state_name)
    dp.message.register(get_name, Command(commands='start'))

    await database_entry()

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(database_entry, 'cron', hour=1, minute=00, start_date='2023-02-16 16:00:00')
    scheduler.start()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except(KeyboardInterrupt, SystemExit):
        print("Error")
