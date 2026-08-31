import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import config
from database.database import init_models
from handlers import base

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Initialize database
    await init_models()
    logger.info("Database initialized.")

    # Initialize bot and dispatcher
    bot = Bot(
        token=config.BOT_TOKEN, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    from scheduler import setup_scheduler
    setup_scheduler(bot)
    
    dp = Dispatcher()

    # Include routers
    from handlers import base, dashboard, tasks, finances, sport
    dp.include_router(base.router)
    dp.include_router(dashboard.router)
    dp.include_router(tasks.router)
    dp.include_router(finances.router)
    dp.include_router(sport.router)

    # Start polling
    logger.info("Bot started polling.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped.")
