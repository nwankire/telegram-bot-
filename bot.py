import os
import sys
import logging
import threading
from flask import Flask, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.error import TelegramError

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
    return jsonify({
        "status": "running",
        "service": "Telegram Bot",
        "platform": "Render"
    })

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# === Environment Debug ===
TOKEN = os.environ.get('BOT_TOKEN')

print("=" * 50)
print("RENDER ENVIRONMENT DEBUG")
print("=" * 50)
print(f"All ENV Keys: {list(os.environ.keys())}")
print(f"BOT_TOKEN in env: {'BOT_TOKEN' in os.environ}")
print(f"TOKEN value: {repr(TOKEN)}")
print(f"PORT: {os.environ.get('PORT', 'Not Set')}")
print("=" * 50)

# === Bot Command Handlers ===
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /start command"""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! 👋\n\n"
        f"I'm <b>alive and running on Render</b> 🚀\n\n"
        f"<b>Commands:</b>\n"
        f"/start - Show this message\n"
        f"/ping - Check if I'm online\n"
        f"/help - Get help\n"
        f"/id - Get your Telegram ID\n\n"
        f"Just send me any message and I'll echo it back!"
    )
    logger.info(f"User {user.id} started the bot")

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /ping command"""
    await update.message.reply_text("Pong! 🏓\nBot is online and responsive!")
    logger.info(f"Ping from user {update.effective_user.id}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /help command"""
    await update.message.reply_html(
        "<b>🤖 Bot Help Menu</b>\n\n"
        "<b>Available Commands:</b>\n"
        "/start - Welcome message\n"
        "/ping - Test bot response\n"
        "/help - This help message\n"
        "/id - Show your Telegram user ID\n"
        "/stats - Bot statistics\n\n"
        "<b>Other Features:</b>\n"
        "• Send any text → I'll echo it back\n"
        "• 24/7 uptime on Render\n\n"
        "Need more help? Contact the bot owner."
    )

async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /id command"""
    user = update.effective_user
    chat = update.effective_chat
    await update.message.reply_html(
        f"<b>Your Info:</b>\n"
        f"User ID: <code>{user.id}</code>\n"
        f"Username: @{user.username if user.username else 'None'}\n"
        f"Chat ID: <code>{chat.id}</code>\n"
        f"Chat Type: {chat.type}"
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /stats command"""
    await update.message.reply_html(
        f"<b>📊 Bot Stats</b>\n\n"
        f"Status: ✅ Online\n"
        f"Platform: Render\n"
        f"Library: python-telegram-bot v20.7\n"
        f"Uptime: 24/7"
    )

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo any text message"""
    user_text = update.message.text
    await update.message.reply_text(f"Echo: {user_text}")
    logger.info(f"Echoed message from {update.effective_user.id}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by Updates"""
    logger.error(f"Update {update} caused error {context.error}")

# === Main Bot Function ===
def run_bot():
    if not TOKEN:
        logger.error("BOT_TOKEN environment variable not found!")
        logger.error("Add BOT_TOKEN in Render → Environment tab")
        logger.error("Make sure there are NO spaces in the key name")
        sys.exit(1)
    
    logger.info(f"Token loaded successfully: {TOKEN[:4]}...{TOKEN[-4:]}")
    
    try:
        # Build application
        application = ApplicationBuilder().token(TOKEN).build()
        
        # Register handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("ping", ping_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("id", id_command))
        application.add_handler(CommandHandler("stats", stats_command))
        
        # Echo handler - must be last
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
        
        # Error handler
        application.add_error_handler(error_handler)
        
        logger.info("Bot handlers registered successfully")
        logger.info("Starting bot polling...")
        logger.info("Send /start to your bot on Telegram to test!")
        
        # Start polling - this blocks
        application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
        
    except TelegramError as e:
        logger.error(f"Telegram error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

# === Entry Point ===
if __name__ == '__main__':
    # Start Flask in daemon thread so Render sees open port
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("Flask thread started")
    
    # Run bot in main thread
    run_bot()
