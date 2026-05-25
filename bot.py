import os
import sys
import logging
import threading
import time
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Flask for Render Port Binding ===
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

@app.route('/health')
def health():
    return "OK"

def start_flask():
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting Flask on port {port}")
    # Use waitress or gunicorn instead of app.run() to avoid blocking
    from waitress import serve
    serve(app, host='0.0.0.0', port=port)

# === Environment ===
TOKEN = os.environ.get('BOT_TOKEN')
print("=" * 50)
print("BOT_TOKEN exists:", 'BOT_TOKEN' in os.environ)
print("TOKEN:", repr(TOKEN))
print("=" * 50)

# === Telegram Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is working! 🚀\nSend /ping")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong! 🏓")

# === Main ===
if __name__ == '__main__':
    if not TOKEN:
        logger.error("No BOT_TOKEN!")
        sys.exit(1)
    
    logger.info(f"Token loaded: {TOKEN[:4]}...{TOKEN[-4:]}")
    
    # Start Flask in daemon thread
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()
    
    # Give Flask 2 seconds to bind port for Render
    time.sleep(2)
    
    # Run bot in MAIN thread - this fixes the crash
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ping", ping))
    
    logger.info("Starting bot polling...")
    application.run_polling(drop_pending_updates=True)
