import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web
import google.generativeai as genai

# Load env vars
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Setup bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Setup Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-pro")

# /start command
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("""🌙✨ Welcome to PromptonAi✨🌙 created by @herox_001
“Your pocket-sized mind companion.”

Hey dreamer 👁‍🗨
I’m PROMPTON, an AI crafted to understand your thoughts, answer your questions, and maybe—just maybe—make the world feel a little less silent.

🕯 What I can do:
– Chat about anything
– Help with ideas, thoughts, or deep questions
– Be your late-night thinking buddy

🔮 Type /help to begin your journey.
Let’s talk... the universe is listening 🌌""")

# /help command
@dp.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("""🛠 **Help Menu**

Here’s what I can do:
/start – Aesthetic welcome message
/help – Show this help menu
<your message> – I will reply like ChatGPT using AI 💬

Just type anything and let’s begin our conversation! ✨""")

# Main AI response handler using Gemini
@dp.message(F.text)
async def gemini_reply(message: types.Message):
    try:
        user_input = message.text
        response = model.generate_content(user_input)
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"⚠️ AI error: {str(e)}")

# Webhook setup
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)

async def on_shutdown(app):
    await bot.delete_webhook()

def create_app():
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app

if __name__ == "__main__":
    app = create_app()
    web.run_app(app, port=int(os.getenv("PORT", 8080)))
