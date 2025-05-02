import logging
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import openai
from collections import defaultdict, deque

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
user_languages = {}
user_histories = defaultdict(lambda: deque(maxlen=5))
LANG_SELECT = range(1)

languages = {
    "English 🇬🇧": "English",
    "Arabic 🇦🇪": "Arabic",
    "Hindi 🇮🇳": "Hindi",
    "Urdu 🇵🇰": "Urdu",
    "Russian 🇷🇺": "Russian",
    "Chinese 🇨🇳": "Chinese",
    "French 🇫🇷": "French",
    "German 🇩🇪": "German"
}

def get_menu(language):
    return ReplyKeyboardMarkup([["Change Language"]], resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_languages[user_id] = "English"

    welcome_message = """
👋 *Welcome to Dubai Guide AI — Your Personal Dubai Travel Assistant!*

I can help you with:

🏝️ Top Attractions
🏨 Hotels & Accommodation
🍽️ Food & Dining
🎉 Events & Activities
📄 Visa Information
🚕 Getting Around Dubai

Just type your question and I'll help in your language!

🌍 To change language, tap "Change Language" anytime.
"""

    await update.message.reply_text(welcome_message, parse_mode="Markdown", reply_markup=get_menu("English"))

async def choose_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌍 Please choose your language:", reply_markup=ReplyKeyboardMarkup(
        [[lang] for lang in languages.keys()], resize_keyboard=True))
    return LANG_SELECT

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    selected = update.message.text.strip()
    if selected in languages:
        lang_name = languages[selected]
        user_languages[user_id] = lang_name
        await update.message.reply_text(f"✅ Language set to {lang_name}", reply_markup=get_menu(lang_name))
    else:
        await update.message.reply_text("❌ Invalid selection.")
    return ConversationHandler.END

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text.strip()
    lang = user_languages.get(user_id, "English")

    all_change_texts = ["Change Language"]
    if user_text in all_change_texts:
        return await choose_language(update, context)

    user_histories[user_id].append({"role": "user", "content": user_text})

    context_messages = [{"role": "system", "content": f"You are Dubai Guide AI, a friendly and helpful Dubai tourism assistant replying in {lang}. Be natural, suggestive, and conversational."}] + list(user_histories[user_id])

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=context_messages,
        timeout=10
    )

    bot_reply = response['choices'][0]['message']['content']
    user_histories[user_id].append({"role": "assistant", "content": bot_reply})

    await update.message.reply_text(bot_reply, reply_markup=get_menu(lang), parse_mode="Markdown")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    lang_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex(".*Change Language.*"), choose_language)],
        states={LANG_SELECT: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_language)]},
        fallbacks=[]
    )

    app.add_handler(lang_conv)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()