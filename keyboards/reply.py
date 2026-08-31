from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import config

def get_main_menu() -> ReplyKeyboardMarkup:
    """Returns the main menu reply keyboard."""
    webapp_url = f"{config.WEBHOOK_HOST}/webapp/index.html" if config.WEBHOOK_HOST else "https://example.com"
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔥 Дашборд"),
                KeyboardButton(text="📝 Планировщик (Mini App)", web_app=WebAppInfo(url=webapp_url))
            ],
            [
                KeyboardButton(text="💰 Финансы"),
                KeyboardButton(text="🎯 Цели")
            ],
            [
                KeyboardButton(text="🏋️ Спорт"),
                KeyboardButton(text="🧠 Проекты & Учеба")
            ],
            [
                KeyboardButton(text="🗣 Получить пинок (ИИ)")
            ]
        ],
        resize_keyboard=True,
        persistent=True
    )
    return keyboard
