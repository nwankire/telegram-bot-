import os
from flask import Flask
from threading import Thread
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = os.environ.get('8823352913:AAHHkvknLOa3wlJRfEyD9yjuz7lRnwUH1Zo')
print(f"Token loaded: {TOKEN[:10]}...") 
# Fake web server so Render Free Web Service stays alive
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram bot is running!"

def run_flask():
  app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))

async def start(update, context):
    await update.message.reply_text('Hello! Bot is online 24/7 🔥')

async def echo(update, context):
    await update.message.reply_text(f'You said: {update.message.text}')

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    print("Bot polling started...")
    application.run_polling()

if __name__ == '__main__':
    Thread(target=run_flask).start()  # Keeps Render happy
    run_bot()  # Runs your actual bot
