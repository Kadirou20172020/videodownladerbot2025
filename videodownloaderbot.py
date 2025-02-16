import os
import logging
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Configuration
TOKEN = "7876030932:AAFw76l_QjGrCjfswtIkwCWYw4LCC7Amq5E"
ALLOWED_DOMAINS = ['youtube.com', 'youtu.be', 'instagram.com', 'facebook.com', 'fb.watch', 'tiktok.com']

def is_valid_url(url: str) -> bool:
    return any(domain in url for domain in ALLOWED_DOMAINS)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🖐 Welcome to Video Downloader Bot!\n\n"
        "Send me a link from:\n"
        "- YouTube\n- Instagram\n- Facebook\n- TikTok\n"
        "And I'll download the video for you!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    user = update.effective_user
    
    if not is_valid_url(url):
        await update.message.reply_text("❌ Unsupported platform. Please send a valid URL from YouTube, Instagram, Facebook, or TikTok.")
        return

    try:
        await update.message.reply_text("⏳ Downloading your video...")
        
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': 'downloaded_video.%(ext)s',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await update.message.reply_video(
            video=open(filename, 'rb'),
            caption="Here's your video! 🎬"
        )
        os.remove(filename)

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("❌ Failed to download video. Please check the link and try again.")
        if os.path.exists(filename):
            os.remove(filename)

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()