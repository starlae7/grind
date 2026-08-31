from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy import select
from database.database import AsyncSessionLocal
from database.models import Finance, FinanceType

router = Router()

@router.message(F.text == "💰 Финансы")
async def cmd_finances(message: Message):
    user_id = message.from_user.id
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Finance).where(Finance.user_id == user_id)
        )
        finances = result.scalars().all()
        
        income = sum(f.amount for f in finances if f.type == FinanceType.INCOME)
        expense = sum(f.amount for f in finances if f.type == FinanceType.EXPENSE)
        assets = [f for f in finances if f.type == FinanceType.ASSET]
        
        text = (
            "<b>💰 ТВОИ ФИНАНСЫ И ИМУЩЕСТВО:</b>\n\n"
            f"🟢 <b>Доходы:</b> {income}\n"
            f"🔴 <b>Расходы:</b> {expense}\n\n"
            "🏠 <b>Активы (Имущество):</b>\n"
        )
        
        if not assets:
            text += "<i>У тебя ничего нет. Ты бомж в Матрице.</i>\n"
        else:
            for a in assets:
                text += f"- {a.name} (Стоимость: {a.amount})\n"
                
        text += (
            "\n<i>Команды для управления:</i>\n"
            "<code>+доход [сумма]</code>\n"
            "<code>+расход [сумма]</code>\n"
            "<code>+актив [название] [сумма]</code>"
        )
        
        await message.answer(text)

@router.message(F.text.lower().startswith("+доход"))
async def add_income(message: Message):
    user_id = message.from_user.id
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].replace('.','',1).isdigit():
        await message.answer("Формат: <code>+доход 5000</code>")
        return
        
    amount = float(parts[1])
    async with AsyncSessionLocal() as session:
        f = Finance(user_id=user_id, type=FinanceType.INCOME, name="Доход", amount=amount)
        session.add(f)
        await session.commit()
    await message.answer(f"Доход {amount} добавлен. Работай усерднее.")

@router.message(F.text.lower().startswith("+расход"))
async def add_expense(message: Message):
    user_id = message.from_user.id
    parts = message.text.split()
    if len(parts) < 2 or not parts[1].replace('.','',1).isdigit():
        await message.answer("Формат: <code>+расход 5000</code>")
        return
        
    amount = float(parts[1])
    async with AsyncSessionLocal() as session:
        f = Finance(user_id=user_id, type=FinanceType.EXPENSE, name="Расход", amount=amount)
        session.add(f)
        await session.commit()
    await message.answer(f"Расход {amount} добавлен. Перестань тратить на фигню.")

@router.message(F.text.lower().startswith("+актив"))
async def add_asset(message: Message):
    user_id = message.from_user.id
    parts = message.text.split()
    if len(parts) < 3 or not parts[-1].replace('.','',1).isdigit():
        await message.answer("Формат: <code>+актив [Название] [стоимость]</code>, например <code>+актив Машина 500000</code>")
        return
        
    amount = float(parts[-1])
    name = " ".join(parts[1:-1])
    async with AsyncSessionLocal() as session:
        f = Finance(user_id=user_id, type=FinanceType.ASSET, name=name, amount=amount)
        session.add(f)
        await session.commit()
    await message.answer(f"Актив '{name}' ({amount}) добавлен. Молодец, хоть что-то заработал.")
