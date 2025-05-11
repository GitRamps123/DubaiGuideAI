
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import openai
import os

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

openai.api_key = os.getenv("OPENAI_API_KEY")

# Simple memory dictionary
conversation_memory = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    user_message = update.message.text

    past_memory = conversation_memory.get(user_id, "")
    prompt = f"You are a helpful assistant for Dubai travel information. Previous: {past_memory}\nUser: {user_message}\nAssistant:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Only answer questions related to Dubai. If the query is not about Dubai, politely redirect to Dubai-related topics."},
            {"role": "user", "content": prompt}
        ]
    )

    reply = response['choices'][0]['message']['content'].strip()
    conversation_memory[user_id] = (past_memory + f"\nUser: {user_message}\nAssistant: {reply}")[-1000:]

    await update.message.reply_text(reply)

def main():
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
