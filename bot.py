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
        f"<b>Commands:</b>\n"
        f"/start - Show this message\n"
        f"/ping - Check if I'm online\n"
        f"/help - Get help\n"
        f"/id - Get your Telegram ID\n\n"
        f"Just send me any message and I'll echo it back!"
    )
    logger.info(f"User {user.id} started the bot")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong! 🏓\nBot
