import os
import openai
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

WELCOME_MESSAGE = "👋 Welcome to the Dubai Guide AI! Ask me anything about Dubai 🌆 (hotels, transport, attractions, food, and more)."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(f"Hi {user.mention_html()}!\n{WELCOME_MESSAGE}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    messages = [
        {"role": "system", "content": "You are a friendly and smart Dubai tourist guide. Only answer questions related to Dubai. If the question is not related to Dubai, politely say you specialize in Dubai-related queries."},
        {"role": "user", "content": user_message}
    ]
    response = openai.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
