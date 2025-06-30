import os
import yt_dlp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from aiohttp import web

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Create downloads folder if not exists
os.makedirs("downloads", exist_ok=True)

# Setup bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# /start command
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("""🎧 Welcome to MP3Bot by @herox_001

📝 Just send a song name or YouTube link and I'll send you an MP3 🎵
Example: `Tum Mile` or `https://youtu.be/xyz...`

⚙️ Powered by yt-dlp & aiogram
""")

# /help command
@dp.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer("""🛠 **Help Menu**

▶️ Just type any song name or paste a YouTube link.

I'll download the audio in MP3 format and send it to you.

🎵 Example:
- *Tum Mile*
- *https://youtu.be/xyz123*

Please be patient while I fetch the song!""")

# Song downloader handler
@dp.message(F.text)
async def handle_song_request(message: types.Message):
    query = message.text.strip()
    await message.answer("🔎 Searching and downloading... Please wait ⏳")
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
            'noplaylist': True,
            'default_search': 'ytsearch1',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=True)
            filename = ydl.prepare_filename(info).replace(".webm", ".mp3").replace(".m4a", ".mp3")

        title = info.get("title", "Song")

        await message.answer_audio(types.FSInputFile(filename), title=title)
        os.remove(filename)

    except Exception as e:
        await message.answer(f"❌ Error: {e}")

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
