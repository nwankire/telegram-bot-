import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# === Flask App to keep Render Web Service alive ===
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram Bot is running on Render! ✅"

@app.route('/health')
def health():
    return "OK", 200

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# === Telegram Bot Setup ===
TOKEN = os.environ.get('8823352913:AAHEXnS0FxKLIFeir3N_xdg_W2vD3aKXS1Y')

# DEBUG LINES - These will tell us why Render can't see BOT_TOKEN
print("=== RENDER DEBUG START ===")
print("RENDER ENV KEYS:", list(os.environ.keys()))
print("BOT_TOKEN EXISTS:", 'BOT_TOKEN' in os.environ)
print("TOKEN VALUE:", repr(TOKEN))
print("=== RENDER DEBUG END ===")

# === Bot Command Functions ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Hello {user_name}! 👋\n\n"
        f"I'm alive and running on Render!\n"
        f"Use /ping to test me."
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong! 🏓 Bot is working perfectly!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

async def help_command(update: Update, context: ContextTypes
