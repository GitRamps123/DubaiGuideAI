
# Dubai Guide AI Bot
import openai
import telegram
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

async def start(update, context):
    await update.message.reply_text("👋 Welcome to Dubai Guide AI — Your Personal Dubai Travel Assistant!\n\n"
                                    "I can help you with:\n"
                                    "🌴 Top Attractions\n🏨 Hotels & Accommodation\n🍽️ Food & Dining\n🎉 Events & Activities\n📄 Visa Information\n🚕 Getting Around Dubai\n\n"
                                    "Just type your question and I'll help in your language!")

async def handle_message(update, context):
    user_message = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}],
        temperature=0.7,
        max_tokens=500
    )
    reply = response.choices[0].message['content']
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()
