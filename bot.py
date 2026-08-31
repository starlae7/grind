import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

import config
from database.database import init_models
from scheduler import setup_scheduler
from handlers import base, dashboard, tasks, finances, sport

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WEBHOOK_PATH = "/webhook"

async def on_startup(bot: Bot):
    await init_models()
    logger.info("Database initialized.")
    
    # Setup webhook if WEBHOOK_HOST is provided
    if config.WEBHOOK_HOST:
        webhook_url = f"{config.WEBHOOK_HOST}{WEBHOOK_PATH}"
        await bot.set_webhook(webhook_url)
        logger.info(f"Webhook set to {webhook_url}")
    else:
        logger.warning("WEBHOOK_HOST is not set. Webhook will not be configured.")

    setup_scheduler(bot)

async def on_shutdown(bot: Bot):
    await bot.delete_webhook()
    logger.info("Webhook deleted. Shutting down.")

def main():
    bot = Bot(
        token=config.BOT_TOKEN, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Include routers
    dp.include_router(base.router)
    dp.include_router(dashboard.router)
    dp.include_router(tasks.router)
    dp.include_router(finances.router)
    dp.include_router(sport.router)

    # Create aiohttp web application
    app = web.Application()
    
    # Register webhook handler
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)

    # Serve the webapp folder as static files
    # This allows the Mini App to be accessible at https://<domain>/webapp/index.html
    current_dir = os.path.dirname(os.path.abspath(__file__))
    webapp_dir = os.path.join(current_dir, "webapp")
    app.router.add_static("/webapp", path=webapp_dir, name="webapp")

    # Bothost usually passes the port in the PORT environment variable
    # If not, fallback to 3000 to match Bothost default
    port = int(os.getenv("PORT", 3000))
    logger.info(f"Starting web server on port {port}")
    
    web.run_app(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
