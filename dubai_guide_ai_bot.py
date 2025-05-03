
import logging
import telegram.ext
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from openai import OpenAI
import os

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update, context):
    welcome_message = (
        "👋 Welcome to Dubai Guide AI — Your Personal Dubai Travel Assistant!\n\n"
        "I can help you with:\n\n"
        "🏝️ Top Attractions\n"
        "🏨 Hotels & Accommodation\n"
        "🍽️ Food & Dining\n"
        "🎉 Events & Activities\n"
        "📄 Visa Information\n"
        "🚕 Getting Around Dubai\n\n"
        "Just type your question and I'll help in your language!\n\n"
        "🌍 To change language, tap \"Change Language\" anytime."
    )
    await update.message.reply_text(welcome_message)

async def handle_message(update, context):
    user_message = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"Error handling message: {e}")
        await update.message.reply_text("Sorry, something went wrong. Please try again later.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot started!")
    app.run_polling()

