from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

def get_main_menu() -> ReplyKeyboardMarkup:
    """Returns the main menu reply keyboard."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔥 Дашборд"),
                # ВАЖНО: Замените URL на ваш, когда зальете webapp на GitHub Pages (например, https://вашин.github.io/magical-nobel/webapp/index.html)
                KeyboardButton(text="📝 Планировщик (Mini App)", web_app=WebAppInfo(url="https://example.com"))
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
