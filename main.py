import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g. https://your-app.onrender.com/webhook

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("🌙✨ Welcome to @LunaWhisperBot ✨🌙 created by @herox_001
“Your pocket-sized mind companion.”

Hey dreamer 👁‍🗨
I’m Luna, an AI crafted to understand your thoughts, answer your questions, and maybe—just maybe—make the world feel a little less silent.

🕯 What I can do:
– Chat about anything
– Help with ideas, thoughts, or deep questions
– Be your late-night thinking buddy

🔮 Type /help to begin your journey.
Let’s talk... the universe is listening 🌌")

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
