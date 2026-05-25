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
    logger.info(f"Starting Flask on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

TOKEN = os.environ.get('BOT_TOKEN')

print("=" * 50)
print("RENDER ENVIRONMENT DEBUG")
print("=" * 50)
print(f"All ENV Keys: {list(os.environ.keys())}")
print(f"BOT_TOKEN exists: {'BOT_TOKEN' in os.environ}")
print(f"TOKEN value: {repr(TOKEN)}")
print("=" * 50)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}! 👋\n\n"
        f"I'm <b>alive on Render</b> 🚀\n\n"
        f"/ping - Test me\n"
        f"/help - Commands\n"
        f"/id - Your Telegram ID"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong! 🏓 Bot is online!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_html(
        "<b>Commands:</b>\n"
        "/start - Start bot\n"
        "/ping - Test bot\n"
        "/help - This menu\n"
        "/id - Get your ID"
    )

async def id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_html(
        f"<b>Your Info:</b>\n"
        f"User ID: <code>{user.id}</code>\n"
        f"Username: @{user.username if user.username else 'None'}"
    )

async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Echo: {update.message.text}")

def run_bot():
    if not TOKEN:
        logger.error("BOT_TOKEN environment variable not found!")
        logger.error("Add BOT_TOKEN in Render → Environment tab")
        sys.exit(1)
    
    logger.info(f"Token loaded: {TOKEN[:4]}...{TOKEN[-4:]}")
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ping", ping))
    application.add
