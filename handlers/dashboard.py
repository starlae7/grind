from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select, func
from database.database import AsyncSessionLocal
from database.models import User, Task, TaskStatus, Finance, FinanceType

router = Router()

@router.message(F.text == "🔥 Дашборд")
async def cmd_dashboard(message: Message):
    user_id = message.from_user.id
    
    async with AsyncSessionLocal() as session:
        # Get User Balance
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            await message.answer("User not found.")
            return

        # Get tasks stats
        tasks_result = await session.execute(
            select(Task.status, func.count(Task.id))
            .where(Task.user_id == user_id)
            .group_by(Task.status)
        )
        tasks_stats = dict(tasks_result.all())
        completed_tasks = tasks_stats.get(TaskStatus.DONE, 0)
        pending_tasks = tasks_stats.get(TaskStatus.PENDING, 0)

        # Get Finances stats
        finances_result = await session.execute(
            select(Finance.type, func.sum(Finance.amount))
            .where(Finance.user_id == user_id)
            .group_by(Finance.type)
        )
        finances_stats = dict(finances_result.all())
        income = finances_stats.get(FinanceType.INCOME, 0.0) or 0.0
        expense = finances_stats.get(FinanceType.EXPENSE, 0.0) or 0.0

        dashboard_text = (
            "<b>🔥 ДАШБОРД (ТВОИ РЕЗУЛЬТАТЫ) 🔥</b>\n\n"
            f"💰 <b>Баланс валюты бота:</b> {user.balance} $\n"
            f"✅ <b>Выполнено задач:</b> {completed_tasks}\n"
            f"⏳ <b>Ожидают выполнения:</b> {pending_tasks}\n\n"
            f"💵 <b>Реальные доходы:</b> {income} RUB/USD\n"
            f"💸 <b>Реальные расходы:</b> {expense} RUB/USD\n\n"
            "<i>Твои результаты — это единственное, что имеет значение. Продолжай работать.</i>"
        )
        
        await message.answer(dashboard_text)
