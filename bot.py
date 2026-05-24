import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get('8823352913:AAEo3NB-UtAF0rgj5CxPMq_30BkHfQ6Guhw')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! 👋 I'm alive on Render FREE hosting.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    PORT = int(os.environ.get('PORT', 10000))
    app.run_polling()  # ← This fixes the Render crash

if __name__ == '__main__':
    main()
