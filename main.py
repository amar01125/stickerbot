import os
import subprocess
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web

# Load env vars
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Ensure downloads folder exists
os.makedirs("downloads", exist_ok=True)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("""🎧 Welcome to Spotify MP3Bot

📝 Send a Spotify link (track/album/playlist)
and I'll reply with the MP3 file(s) 🎶

⚙️ Powered by spotdl & aiogram
""")

@dp.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("""🛠 Help Menu

▶️ Paste a Spotify link (track/album/playlist).

I'll fetch the audio in MP3 format and send it to you.

🎵 Example:
- https://open.spotify.com/track/xyz
- https://open.spotify.com/playlist/abc

Please wait while I fetch your music.
""")

@dp.message(F.text)
async def handle_song_request(message: types.Message):
    url = message.text.strip()
    await message.answer("🔎 Fetching from Spotify... Please wait ⏳")
    try:
        # Run spotdl to download to downloads folder
        subprocess.run([
            "spotdl", url,
            "--output", "downloads/{title}.{output-ext}",
            "--format", "mp3"
        ], check=True)

        # Send all .mp3 files in downloads folder
        for file in os.listdir("downloads"):
            if file.endswith(".mp3"):
                filepath = os.path.join("downloads", file)
                await message.answer_audio(types.FSInputFile(filepath), title=file.replace(".mp3", ""))
                os.remove(filepath)

    except subprocess.CalledProcessError as e:
        await message.answer(f"❌ Error downloading: {e}")

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
