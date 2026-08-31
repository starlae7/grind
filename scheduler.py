from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot
from sqlalchemy import select
from database.database import AsyncSessionLocal
from database.models import User
from services.ai_motivator import generate_motivation
import logging

logger = logging.getLogger(__name__)

async def send_morning_kick(bot: Bot):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User.id))
        users = result.scalars().all()
        
        quote = await generate_motivation("It is morning. Tell them to wake up and start working.")
        for user_id in users:
            try:
                await bot.send_message(user_id, quote)
            except Exception as e:
                logger.error(f"Failed to send kick to {user_id}: {e}")

async def send_evening_review(bot: Bot):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User.id))
        users = result.scalars().all()
        
        quote = await generate_motivation("It is evening. Tell them to reflect on their day and prepare for tomorrow.")
        for user_id in users:
            try:
                await bot.send_message(user_id, quote)
            except Exception as e:
                logger.error(f"Failed to send review to {user_id}: {e}")

def setup_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler()
    # Schedule morning kick at 8:00
    scheduler.add_job(send_morning_kick, CronTrigger(hour=8, minute=0), kwargs={"bot": bot})
    # Schedule evening review at 21:00
    scheduler.add_job(send_evening_review, CronTrigger(hour=21, minute=0), kwargs={"bot": bot})
    
    scheduler.start()
    logger.info("Scheduler started.")
