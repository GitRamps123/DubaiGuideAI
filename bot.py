
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# In-memory conversation history per user
conversation_memory = {}

def update_conversation(user_id, user_msg, bot_msg=None):
    if user_id not in conversation_memory:
        conversation_memory[user_id] = []
    conversation_memory[user_id].append({"user": user_msg, "bot": bot_msg})
    if len(conversation_memory[user_id]) > 10:
        conversation_memory[user_id].pop(0)

def get_last_bot_message(user_id):
    if user_id in conversation_memory and conversation_memory[user_id]:
        return conversation_memory[user_id][-1]['bot']
    return ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "👋 Welcome to Dubai Guide AI — Your Personal Dubai Travel Assistant!

I can help you with:
🌴 Top Attractions
🏨 Hotels & Accommodation
🍽️ Food & Dining
🎉 Events & Activities
📄 Visa Information
🚕 Getting Around Dubai

Just type your question and I'll help in your language!"
    await update.message.reply_text(welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    previous_bot_message = get_last_bot_message(user_id)

    # Build prompt with context
    prompt = f"Previous Bot Message: {previous_bot_message}
User: {user_message}
Bot:"

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    reply = response["choices"][0]["message"]["content"].strip()

    await update.message.reply_text(reply)
    update_conversation(user_id, user_message, reply)

def main():
    application = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == "__main__":
    main()
