import os
from flask import Flask
from threading import Thread
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = os.environ.get('8823352913:AAHHkvknLOa3wlJRfEyD9yjuz7lRnwUH1Zo')

# Fake web server to keep Render Web Service alive
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
  app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

async def start(update, context):
    await update.message.reply_text('Hello! I am alive.')

async def echo(update, context):
    await update.message.reply_text(f'You said: {update.message.text}')

def run_bot():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.run_polling()

if __name__ == '__main__':
    Thread(target=run_flask).start()  # Start web server
    run_bot()  # Start Telegram bot
