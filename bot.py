import os
import sys
import logging
import asyncio
from flask import Flask, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.error import TelegramError
from threading import Thread
from werkzeug.serving import make_server

# === Setup Logging ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === Flask App for Render Health Checks ===
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "running", "service": "Telegram Bot"})

@app.route('/health')
def health():
    return "OK", 200

# === Flask in Separate Thread - No Asyncio Conflict ===
class FlaskThread(Thread):
    def __init__(self, app):
        Thread.__init__(self)
        self.server = make_server('0.0.0.0', int(os.environ.get('PORT', 10000)), app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        logger.info(f"Starting Flask server on port {os.environ.get('PORT', 10000)}")
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

# === Environment Debug ===
TOKEN = os.environ.get('BOT_TOKEN')

print("=" * 50)
print("RENDER ENVIRONMENT DEBUG")
print("=" * 50)
print(f"BOT_TOKEN exists: {'BOT_TOKEN' in os.environ}")
print(f"TOKEN value: {repr(TOKEN)}")
print(f"PORT: {os.environ.get('PORT', 'Not Set')}")
print("=" * 50)

# === Bot Command Handlers ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! 👋\n\n"
        f"I'm <b>alive and running on Render</b> 🚀\n\n"
        f"<b>Commands:</b>\n/start - Show this\n/ping - Test me\n/help - Help menu"
    )
    logger.info(f"User {user.id} started the bot")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong! 🏓\nBot is online!")
    logger.info(f"Ping from user {update.effective_user.id}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(
        "<b>🤖 Bot Commands</b>\n\n"
        "/start - Welcome\n/ping - Test bot\n/help - This menu"
    )

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Echo: {update.message.text}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")

# === Main Bot Function ===
def run_bot():
    if not TOKEN:
        logger.error("BOT_TOKEN environment variable not found!")
        sys.exit(1)
    
    logger.info(f"Token loaded successfully: {TOKEN[:4]}...{TOKEN[-4:]}")
    
    try:
        application = ApplicationBuilder().token(TOKEN).build()
        
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("ping", ping))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
        application.add_error_handler(error_handler)
        
        logger.info("Starting bot polling...")
        application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
        
    except TelegramError as e:
        logger.error(f"Telegram error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

# === Entry Point ===
if __name__ == '__main__':
    # Start Flask in separate thread using werkzeug
    flask_thread = FlaskThread(app)
    flask_thread.start()
    
    # Run bot in main thread - no asyncio conflict
    try:
        run_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped")
    finally:
        flask_thread.shutdown()
