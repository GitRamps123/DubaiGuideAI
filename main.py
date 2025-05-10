print("Bot is starting...")

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

async def handle_message(update, context):
    user_message = update.message.text
    print(f"Received message: {user_message}")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = "Sorry, I couldn't process your request."
        print(f"Error: {e}")
    await update.message.reply_text(reply)

def main():
    print("Running bot...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
