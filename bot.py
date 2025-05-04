
import logging
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from openai import OpenAI
import os

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Store user short-term memory (in-memory session)
user_sessions = {}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"👋 Hi {user.mention_html()}! Welcome to the Dubai AI Guide. Ask me anything about Dubai - hotels, transport, food, attractions and more. I'm here to make your trip amazing ✨",
        reply_markup=ForceReply(selective=True),
    )

# Helper to generate smart AI responses with context
def generate_ai_reply(user_id, user_message):
    context_memory = user_sessions.get(user_id, {}).get("context", "")

    prompt = f"""
You are Dubai AI Guide Bot, a polite, friendly and helpful assistant. Maintain a natural and warm tone like ChatGPT.
Always act as a Dubai expert. Never ask for vague clarifications. Be proactive and helpful. Assume context.

Current conversation context: {context_memory}

User says: "{user_message}"

Your response (be polite, friendly, praise user choice when relevant, connect answers smoothly to previous topic and avoid confusion):
"""

    completion = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a polite and friendly Dubai tourism assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6
    )

    return completion.choices[0].message.content.strip()

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    user_text = update.message.text

    # Initialize user session if not exists
    if user_id not in user_sessions:
        user_sessions[user_id] = {"context": ""}

    # Append new user query to context
    if user_sessions[user_id]["context"]:
        user_sessions[user_id]["context"] += f" User: {user_text}"
    else:
        user_sessions[user_id]["context"] = f"User: {user_text}"

    # Generate AI reply
    ai_reply = generate_ai_reply(user_id, user_text)

    # Update context with bot response
    user_sessions[user_id]["context"] += f" Bot: {ai_reply}"

    # Send reply
    await update.message.reply_text(ai_reply)

# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Exception while handling update:", exc_info=context.error)

# Main function to run the bot
def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    application = Application.builder().token(token).build()

    # Commands
    application.add_handler(CommandHandler("start", start))

    # Messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors
    application.add_error_handler(error_handler)

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
