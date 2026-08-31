from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select
from database.database import AsyncSessionLocal
from database.models import Task, User, TaskStatus

router = Router()

@router.message(F.text == "📝 Планировщик")
async def cmd_planner(message: Message):
    user_id = message.from_user.id
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Task).where(Task.user_id == user_id, Task.status == TaskStatus.PENDING)
        )
        tasks = result.scalars().all()
        
        if not tasks:
            await message.answer(
                "Твой список задач пуст. Это значит, что ты деградируешь. "
                "Добавь задачу, написав: <code>+задача [Текст задачи]</code>"
            )
            return
            
        tasks_text = "<b>📝 ТВОИ ЗАДАЧИ НА СЕГОДНЯ:</b>\n\n"
        for i, t in enumerate(tasks, 1):
            tasks_text += f"{i}. {t.title} (+{t.reward}$)\n"
            
        tasks_text += "\n<i>Чтобы выполнить, напиши: <code>выполнил [номер]</code></i>"
        
        await message.answer(tasks_text)

@router.message(F.text.lower().startswith("+задача"))
async def cmd_add_task(message: Message):
    user_id = message.from_user.id
    title = message.text[7:].strip()
    
    if not title:
        await message.answer("Ты забыл написать текст задачи. Слабак.")
        return
        
    async with AsyncSessionLocal() as session:
        new_task = Task(user_id=user_id, title=title, reward=10.0)
        session.add(new_task)
        await session.commit()
        
    await message.answer(f"Задача добавлена. Иди и выполняй её. Награда: 10$.")

@router.message(F.text.lower().startswith("выполнил"))
async def cmd_complete_task(message: Message):
    user_id = message.from_user.id
    parts = message.text.split()
    
    if len(parts) < 2 or not parts[1].isdigit():
        await message.answer("Формат: <code>выполнил [номер задачи из списка]</code>")
        return
        
    task_num = int(parts[1]) - 1
    
    async with AsyncSessionLocal() as session:
        # Get tasks in same order
        result = await session.execute(
            select(Task).where(Task.user_id == user_id, Task.status == TaskStatus.PENDING)
        )
        tasks = result.scalars().all()
        
        if task_num < 0 or task_num >= len(tasks):
            await message.answer("Неверный номер задачи.")
            return
            
        task = tasks[task_num]
        task.status = TaskStatus.DONE
        
        # Reward user
        user_result = await session.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one()
        user.balance += task.reward
        
        await session.commit()
        
        await message.answer(f"✅ Задача '{task.title}' выполнена. Тебе начислено {task.reward}$. Продолжай в том же духе.")

import json
@router.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    user_id = message.from_user.id
    try:
        data = json.loads(message.web_app_data.data)
        if data.get('action') == 'add_task':
            title = data.get('title')
            async with AsyncSessionLocal() as session:
                new_task = Task(user_id=user_id, title=title, reward=10.0)
                session.add(new_task)
                await session.commit()
            
            await message.answer(f"Задача '{title}' успешно добавлена через Mini App! Иди выполняй.")
    except Exception as e:
        await message.answer("Ошибка обработки данных из Mini App.")
