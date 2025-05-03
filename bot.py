
from telegram.ext import ApplicationBuilder, CommandHandler
import os

TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.environ.get('PORT', '8443'))

async def start(update, context):
    await update.message.reply_text("👋 Welcome to Come To Dubai AI — your personal Dubai Travel Assistant!

I can help you with:
🌴 Top Attractions
🏨 Hotels & Accommodation
🍽️ Food & Dining
🎉 Events & Activities
📄 Visa Information
🚖 Getting Around Dubai")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

# Setup webhook instead of polling
app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=TOKEN,
    webhook_url=f"https://YOUR-RAILWAY-APP-URL/{TOKEN}"
)
