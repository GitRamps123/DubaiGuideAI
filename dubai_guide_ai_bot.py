
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Initialize OpenAI Client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👋 Welcome to Dubai Guide AI — Your Personal Dubai Travel Assistant!\n\n"
        "I can help you with:\n"
        "🌴 Top Attractions\n"
        "🏨 Hotels & Accommodation\n"
        "🍽️ Food & Dining\n"
        "🎉 Events & Activities\n"
        "📄 Visa Information\n"
        "🚕 Getting Around Dubai\n\n"
        "Just type your question and I'll help in your language!"
    )
    await update.message.reply_text(welcome_text)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    # Call OpenAI Chat Completion
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful travel assistant focused on Dubai."},
            {"role": "user", "content": user_message},
        ]
    )

    reply_text = response.choices[0].message.content
    await update.message.reply_text(reply_text)


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


def main():
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(telegram_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    app.run_polling()


if __name__ == "__main__":
    main()
