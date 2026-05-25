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

# === Telegram
