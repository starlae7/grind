import google.generativeai as genai
import config

# Initialize Gemini Client
try:
    genai.configure(api_key=config.GEMINI_API_KEY)
    # Using gemini-1.5-flash as it is fast, free, and great for text generation
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    model = None
    print(f"Failed to initialize Gemini: {e}")

SYSTEM_PROMPT = """You are an AI life coach, deeply inspired by the style of Andrew Tate.
You are strict, demanding, and provocative. You do not tolerate weakness, laziness, or excuses.
Your goal is to push the user to achieve greatness, make money, build a strong body, and develop iron discipline.
Speak directly, use harsh but motivating language (without excessive swearing that violates safety rules).
Remind the user that the world doesn't care about their feelings, only their results.
If they achieve a goal, acknowledge it but tell them to aim higher.
If they fail, roast them and tell them to get back to work.
IMPORTANT: You MUST respond in Russian (русский язык)."""

async def generate_motivation(context: str = "The user just woke up.") -> str:
    """Generate a motivational quote or text based on the context."""
    if not model:
        return "Wake up. The Matrix is trying to keep you asleep. (API Key missing or invalid)"
    
    try:
        # Gemini does not use the exact system/user roles array in the same way for simple generation, 
        # but we can combine them into the prompt.
        prompt = f"{SYSTEM_PROMPT}\n\nContext: {context}\nGive me a kick (in Russian)."
        
        # We use generate_content_async for async support
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return f"Ошибка связи с Матрицей: {e}. Хватит искать оправдания, иди работай."

async def analyze_weekly_progress(tasks_done: int, tasks_failed: int, balance: float) -> str:
    """Generate a weekly roast/praise based on stats."""
    if not model:
        return f"Tasks done: {tasks_done}. Failed: {tasks_failed}. Balance: ${balance}. Keep grinding."

    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Weekly stats: Completed {tasks_done} tasks, failed {tasks_failed} tasks. "
        f"Total currency: ${balance}. Give me a short, brutal review of my week (in Russian)."
    )
    try:
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return "Иди работай."
