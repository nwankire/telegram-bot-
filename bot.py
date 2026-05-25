import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# 1. Load token safely - no more NoneType crash
TOKEN = os.environ.get('8823352913:AAHEXnS0FxKLIFeir3N_xdg_W2vD3aKXS1Y')

# 2. Create Flask app to keep Render happy
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is alive!"

# 3. Telegram bot commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive on Render 🚀")

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong!")

def main():
    # 4. Check if token exists BEFORE starting
    if not TOKEN:
        print("ERROR: BOT_TOKEN environment variable not found!")
        print("Add BOT_TOKEN in Render → Environment tab")
        return
    
    print(f"Token loaded: {TOKEN[:10]}...")
    
    # 5. Start bot
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ping", ping))
    
    print("Bot polling started...")
    application.run_polling()

if __name__ == '__main__':
    # Run Flask in background for Render web service
    import threading
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))).start()
    main()
