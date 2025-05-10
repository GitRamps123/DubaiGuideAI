
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(level=logging.INFO)

# Simple in-memory context store (for single message memory)
user_context = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to Dubai Guide AI – your friendly travel companion! Ask me anything about Dubai: food, attractions, transport, or hidden gems 🌟.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text

    prev = user_context.get(user_id, {})
    prompt = f"""
You are Dubai Guide AI, a friendly and helpful assistant for tourists in Dubai. Always stay on topic. Be cheerful, warm, and brief. If user asks about other countries, politely redirect to Dubai topics.

Previous question: {prev.get('user', 'N/A')}
Previous answer: {prev.get('bot', 'N/A')}
User follow-up: {user_message}

Answer:
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're Dubai Guide AI. Respond politely and informatively."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=400
        )
        reply = response.choices[0].message.content.strip()

        await update.message.reply_text(reply)

        # Save context
        user_context[user_id] = {"user": user_message, "bot": reply}
    except Exception as e:
        logging.error(e)
        await update.message.reply_text("Oops! Something went wrong. Please try again in a moment.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
