import os
import io
from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Ensure stickers folder exists
os.makedirs("stickers", exist_ok=True)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("""👋 Welcome to StickerMaker Bot

🖊 Send any text — I'll turn it into a sticker
🖼 Send any photo — I'll convert it into a sticker

⚙️ Powered by aiogram & Pillow
""")

@dp.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("""🛠 Help Guide

✅ Send text — Get a text sticker
✅ Send image — Get an image sticker

🔄 Stickers are auto-generated and sent back to you.
""")

@dp.message(F.text)
async def text_to_sticker(message: types.Message):
    text = message.text.strip()
    if not text:
        return

    img = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()

    w, h = draw.textsize(text, font=font)
    draw.text(((512-w)//2, (512-h)//2), text, fill="black", font=font)

    sticker_path = f"stickers/text_{message.message_id}.webp"
    img.save(sticker_path, format="WEBP")

    await message.answer_sticker(types.FSInputFile(sticker_path))
    os.remove(sticker_path)

@dp.message(F.photo)
async def photo_to_sticker(message: types.Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    photo_data = await bot.download_file(file.file_path)

    img = Image.open(io.BytesIO(photo_data.read())).convert("RGBA")
    img = img.resize((512, 512))

    sticker_path = f"stickers/photo_{message.message_id}.webp"
    img.save(sticker_path, format="WEBP")

    await message.answer_sticker(types.FSInputFile(sticker_path))
    os.remove(sticker_path)

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
