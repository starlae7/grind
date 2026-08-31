from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from sqlalchemy import select
from database.database import AsyncSessionLocal
from database.models import User
from keyboards.reply import get_main_menu
from services.ai_motivator import generate_motivation

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command. Registers user if not exists."""
    user_id = message.from_user.id
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            # Register new user
            new_user = User(id=user_id)
            session.add(new_user)
            await session.commit()
            
            welcome_text = (
                "Welcome to the real world. This bot will make you disciplined.\n"
                "You have 0$. Start working to earn respect."
            )
        else:
            welcome_text = "Welcome back. Stop wasting time and get to work."

    await message.answer(welcome_text, reply_markup=get_main_menu())

@router.message(F.text == "🗣 Получить пинок (ИИ)")
async def handle_motivation(message: Message):
    """Generates a Tate-style motivational quote."""
    await message.answer("Analyzing your pathetic existence... wait a second.")
    quote = await generate_motivation("The user is asking for motivation by clicking a button.")
    await message.answer(quote)

@router.message(F.photo)
async def handle_photo(message: Message):
    """Handles photo uploads for motivation."""
    await message.answer("I see your photo. Is this what you want to achieve, or what you currently are? I'll analyze it soon. (AI Vision feature can be connected here)")
    quote = await generate_motivation("The user just uploaded a photo to the bot.")
    await message.answer(quote)
