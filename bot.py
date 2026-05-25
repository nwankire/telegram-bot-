import os
import sys
import logging
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def start_flask():
    from waitress import serve
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting Flask on port {port}")
    serve(app, host='0.0.0.0', port=port)

TOKEN = os.environ.get('BOT_TOKEN')
print("BOT_TOKEN exists:", 'BOT_TOKEN' in os.environ)
print("TOKEN:", repr(TOKEN))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bot is working! 🚀\nSend /ping")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong! 🏓")

if __name__ == '__main__':
    if not TOKEN:
        logger.error("No BOT_TOKEN!")
        sys.exit(1)
    
    logger.info(f"Token: {TOKEN[:4]}...{TOKEN[-4:]}")
    
    threading.Thread(target=start_flask, daemon=True).start()
    
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ping", ping))
    
    logger.info("Starting bot polling...")
    application.run_polling(drop_pending_updates=True)
