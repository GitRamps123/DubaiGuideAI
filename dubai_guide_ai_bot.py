import os
import openai
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

openai.api_key = os.getenv("OPENAI_API_KEY")
SYSTEM_PROMPT = """
You are Dubai Guide AI – a cheerful, helpful, and knowledgeable travel assistant for tourists visiting Dubai.
You specialize in providing fun, friendly, and informative responses about attractions, food, shopping, culture, nightlife, transportation, and visas related to Dubai. Maintain a conversational, engaging tone.
Always try to connect follow-up questions to the previous topic unless the user shifts context.
"""

user_context = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_message = (
        f"👋 Hello and welcome to Dubai Guide AI! 🌟 I’m your personal travel assistant for everything Dubai. "
        f"Ask me about places to visit, food to try, transportation tips, or anything else you’re curious about. 🏖️✈️"
    )
    await update.message.reply_text(welcome_message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_input = update.message.text

    # Track user context
    history = user_context.get(chat_id, [])
    history.append(f"User: {user_input}")
    if len(history) > 6:
        history = history[-6:]  # Keep only the last 6 messages
    user_context[chat_id] = history

    prompt = SYSTEM_PROMPT + "\n" + "\n".join(history) + "\nAssistant:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        reply = response.choices[0].message['content'].strip()
    except Exception as e:
        reply = "I'm sorry, something went wrong. Please try again later."

    history.append(f"Assistant: {reply}")
    user_context[chat_id] = history
    await update.message.reply_text(reply)

def main() -> None:
    application = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()