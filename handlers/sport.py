from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select
from database.database import AsyncSessionLocal
from database.models import Metric, MetricCategory

router = Router()

@router.message(F.text == "🏋️ Спорт")
async def cmd_sport(message: Message):
    user_id = message.from_user.id
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Metric).where(Metric.user_id == user_id, Metric.category == MetricCategory.SPORT)
        )
        metrics = result.scalars().all()
        
        text = "<b>🏋️ ТВОЙ СПОРТ ПРОГРЕСС:</b>\n\n"
        if not metrics:
            text += "<i>Ты ничего не делаешь. Твое тело слабое.</i>\n"
        else:
            for m in metrics:
                text += f"- {m.name}: {m.value}\n"
                
        text += (
            "\n<i>Для добавления результата напиши:</i>\n"
            "<code>+спорт [Упражнение] [значение]</code>\n"
            "<i>Пример: <code>+спорт Отжимания 100</code></i>"
        )
        
        await message.answer(text)

@router.message(F.text.lower().startswith("+спорт"))
async def add_sport(message: Message):
    user_id = message.from_user.id
    parts = message.text.split()
    if len(parts) < 3 or not parts[-1].replace('.','',1).isdigit():
        await message.answer("Формат: <code>+спорт [Упражнение] [значение]</code>")
        return
        
    value = float(parts[-1])
    name = " ".join(parts[1:-1])
    async with AsyncSessionLocal() as session:
        # Update or create
        result = await session.execute(
            select(Metric).where(Metric.user_id == user_id, Metric.category == MetricCategory.SPORT, Metric.name == name)
        )
        metric = result.scalar_one_or_none()
        if metric:
            metric.value += value
        else:
            metric = Metric(user_id=user_id, category=MetricCategory.SPORT, name=name, value=value)
            session.add(metric)
        await session.commit()
        
    await message.answer(f"Твои {name} увеличены на {value}. Продолжай пахать.")
