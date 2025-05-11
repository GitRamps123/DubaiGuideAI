import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import openai
import os

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
openai.api_key = OPENAI_API_KEY

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Store last Q&A for basic memory
user_context = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to Dubai Guide AI! Ask me anything about Dubai 🇦🇪.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text

    # Basic memory
    prev_qa = user_context.get(user_id, {})
    prompt = "You are a polite, friendly Dubai tourist assistant. ONLY answer questions related to Dubai.
"
    if prev_qa:
        prompt += f"Previous Q: {prev_qa['q']}
Previous A: {prev_qa['a']}
"
    prompt += f"User: {message}
AI:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
    )

    reply = response.choices[0].message["content"].strip()
    user_context[user_id] = {"q": message, "a": reply}
    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
