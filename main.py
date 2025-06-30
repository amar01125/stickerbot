import os
from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

# Set your bot token and webhook URL through environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g. https://your-app.onrender.com/webhook

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Welcome!\n\nCreated by @herox_001")

async def on_startup(app):
    # Set webhook on startup
    await bot.set_webhook(WEBHOOK_URL + WEBHOOK_PATH)

async def on_shutdown(app):
    # Remove webhook on shutdown
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
