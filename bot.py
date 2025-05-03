
import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# Context storage
user_context = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome to Dubai Guide AI — Your Personal Dubai Travel Assistant!

"
                                    "I can help you with:
"
                                    "🌴 Top Attractions
"
                                    "🏨 Hotels & Accommodation
"
                                    "🍽️ Food & Dining
"
                                    "🎉 Events & Activities
"
                                    "🛂 Visa Information
"
                                    "🚕 Getting Around Dubai

"
                                    "Just type your question and I'll help in your language!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_input = update.message.text

    # Maintain conversation context
    previous_context = user_context.get(user_id, "")
    prompt = f"You are a friendly Dubai travel assistant helping with tourist info. Previous conversation: {previous_context}
User: {user_input}
AI:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a friendly Dubai tourist guide bot."},
                  {"role": "user", "content": prompt}]
    )

    reply = response['choices'][0]['message']['content']
    await update.message.reply_text(reply)

    # Update context
    user_context[user_id] = f"{previous_context}
User: {user_input}
AI: {reply}"

app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
