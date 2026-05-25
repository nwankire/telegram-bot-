import os
import sys
import logging
import asyncio
from flask import Flask, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from telegram.error import TelegramError
from hypercorn.asyncio import serve
from hypercorn.config import Config

# === Setup Logging ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === Flask App ===
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "running", "service": "Telegram Bot"})

@app.route('/health')
def health():
    return "OK", 200

# ===
