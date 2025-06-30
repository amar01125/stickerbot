import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web
from openai import OpenAI

# Get environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g. https://your-app.onrender.com/webhook
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Initialize OpenAI client (new version syntax)
client = OpenAI(api_key=OPENAI_API_KEY)

# Start command handler
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

# Help command handler
@dp.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("""🛠 **Help Menu**

Here’s what I can do:

/start – Aesthetic welcome message  
/help – Show this help menu  
<your message> – I will reply like ChatGPT using AI 💬

Just type anything and let’s begin our conversation! ✨""")

# Main AI reply handler
@dp.message(F.text)
async def chatgpt_reply(message: types.Message):
    try:
        user_input = message.text
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response.choices[0].message.content
        await message.answer(reply)

    except Exception as e:
        await message.answer(f"⚠️ AI error: {str(e)}")

# Webhook startup and shutdown
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)

async def on_shutdown(app):
    await bot.delete_webhook()

# Create and run aiohttp app
def create_app():
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=WEBHOOK_PATH)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    return app

# Run the app
if __name__ == "__main__":
    app = create_app()
    web.run_app(app, port=int(os.getenv("PORT", 8080)))
