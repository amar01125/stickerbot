import os
import io
import random
from PIL import Image, ImageDraw, ImageFont
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web

BOT_TOKEN = "7972815740:AAHjhjeuO44SB8OK7M-bS_6wDDDewWuPfE8"
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = "https://stickerbot-kvme.onrender.com"

os.makedirs("stickers", exist_ok=True)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("""👋 Welcome to 🤖 StickerMaker Bot!

🎨 I can turn your words, photos, and quotes into cool Telegram stickers.

🔧 Available commands:
  /help - Full guide
  /randomcolor <text> - Sticker with random colors
  /fontlist - View available system fonts
  /q (as reply) - Quote a message as a sticker
  /plain <text> - Text sticker without user info
  /bg <color> <text> - Set custom background color
  /ping - Check bot status

📥 Just send text or an image, and I’ll reply with a sticker!
""")

@dp.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("""🆘 Help Menu: StickerMaker Bot

✅ Auto Features:
  - Send any text: Violet sticker with your name & profile
  - Send any image: Convert photo to sticker

🔧 Manual Commands:
  /randomcolor <text> - Random background + text color
  /fontlist - List available system fonts
  /q (reply) - Create sticker from any replied message
  /plain <text> - Sticker with only your text
  /bg <color> <text> - Custom color background (e.g. /bg red Hello)
  /ping - Check bot is alive

🎨 Available Colors (for /bg command):
  red, green, blue, yellow, orange, violet, purple, white, black, gray, cyan, pink, brown, gold, navy

📌 Notes:
- All stickers are 512×512 WebP
- Usernames and profile photos are auto-added when possible
- Bot deletes files after sending

⚙️ Powered by Python, aiogram & Pillow
""")

@dp.message(Command("plain"))
async def plain_sticker(message: types.Message):
    text = message.text.replace("/plain", "").strip()
    if not text:
        await message.answer("✏️ Provide text after /plain")
        return
    img = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((512 - w) // 2, (512 - h) // 2), text, fill="black", font=font)
    path = f"stickers/plain_{message.message_id}.webp"
    img.save(path, format="WEBP")
    await message.answer_sticker(types.FSInputFile(path))
    os.remove(path)

@dp.message(Command("bg"))
async def bg_color_sticker(message: types.Message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("🖌 Use format: /bg color text — e.g. /bg green Hello")
        return
    _, color, text = args
    img = Image.new("RGBA", (512, 512), color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 60)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((512 - w) // 2, (512 - h) // 2), text, fill="white", font=font)
    path = f"stickers/bg_{message.message_id}.webp"
    img.save(path, format="WEBP")
    await message.answer_sticker(types.FSInputFile(path))
    os.remove(path)

@dp.message(Command("ping"))
async def ping(message: types.Message):
    await message.answer("🏓 Bot is alive!")

# [Other command handlers remain unchanged and continue below here...]

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
