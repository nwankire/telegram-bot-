import os
import sys
import logging
import threading
from flask import Flask, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "running", "service": "Telegram Bot"})

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

TOKEN = os.environ.get('BOT_TOKEN')

print("=" * 50)
print("RENDER ENVIRONMENT DEBUG")
print("=" * 50)
print(f"BOT_TOKEN exists: {'BOT_TOKEN' in os.environ}")
print(f"TOKEN value: {repr(TOKEN)}")
print("=" * 50)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! 👋\n\n"
        f"I'm <b>alive and running on Render</b> 🚀\n\n"
        f"/ping - Test me\n"
        f"/help - Commands"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong! 🏓\nBot is online and responsive!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(
        "<b>Commands:</b>\n"
        "/start - Start bot\n"
        "/ping - Test bot\n"
        "/help - This menu"
    )

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Echo: {update.message.text}")

def run_bot():
    if not TOKEN:
        logger.error("BOT_TOKEN environment variable not found!")
        sys.exit(1)
    
    logger.info(f"Token loaded: {TOKEN[:4]}...{TOKEN[-4:]}")
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add
