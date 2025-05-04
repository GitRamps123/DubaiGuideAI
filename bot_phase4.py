
# Dubai AI Bot - Phase 4 (Conversational and Memory Enhanced Version)
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

openai.api_key = OPENAI_API_KEY

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# In-memory user history (temporary memory)
user_sessions = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("👋 Welcome to Dubai Guide AI! Ask me anything about Dubai — attractions, hotels, food, visas and more.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    user_message = update.message.text

    # Load previous conversation
    messages = user_sessions.get(user_id, [{"role": "system", "content": "You are Dubai Guide AI. Be friendly, helpful, conversational and give travel guidance."}])

    # Add user message
    messages.append({"role": "user", "content": user_message})

    try:
        # Send to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )

        bot_reply = response['choices'][0]['message']['content']

        # Save bot reply to history
        messages.append({"role": "assistant", "content": bot_reply})

        # Save updated messages
        user_sessions[user_id] = messages[-10:]  # Keep last 10 for memory

        await update.message.reply_text(bot_reply)

    except Exception as e:
        await update.message.reply_text("⚠️ There was an error. Please try again later.")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()

if __name__ == "__main__":
    main()
