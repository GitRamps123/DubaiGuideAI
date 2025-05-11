import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Memory buffer to store last message context
context_memory = {}

# Friendly and engaging prompt style
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hello and welcome to Dubai Guide AI! 🌟 I’m your personal travel assistant for everything Dubai. Ask me about places to visit, food to try, transportation tips, or anything else you’re curious about. 🏖️✈️")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text.strip().lower()

    last_context = context_memory.get(user_id, "")

    response = ""

    if "white dubai" in user_message:
        response = "🎶 White Dubai is a popular nightclub in Meydan, Dubai, known for great music, a lively crowd, and stunning skyline views. Perfect for a high-energy night out!"
    elif "cost" in user_message or "price" in user_message:
        if "white dubai" in last_context:
            response = "💳 Entry to White Dubai often depends on the night and event. Expect a minimum spend around AED 300–500 on busy nights."
        else:
            response = "💰 Entry costs vary depending on the venue or activity. Could you tell me which place you’re referring to?"
    elif "restaurants" in user_message:
        response = "🍽️ Dubai has incredible restaurants! Try Zuma for Japanese cuisine, Al Hadheerah for traditional Emirati vibes, or Pierchic for a romantic seafood dinner with sea views. Would you like options by location or cuisine?"
    elif "zuma" in user_message:
        response = "📍 Zuma is located in Dubai International Financial Centre (DIFC). It’s stylish, upscale, and well-loved for its creative twist on traditional Japanese dishes."
    elif "visa" in user_message:
        response = "🛂 Visa requirements depend on your nationality. You can visit [https://www.gdrfad.gov.ae](https://www.gdrfad.gov.ae) — the official Dubai immigration portal — for up-to-date details."
    elif "1" in user_message or "item 1" in user_message:
        if "rove" in last_context or "hotels" in last_context:
            response = "🏨 Rove Downtown typically costs around AED 250–400 per night depending on the season. It’s modern, clean, and just steps from the Dubai Mall."
        else:
            response = "🔍 Could you please clarify what '1' refers to?"
    elif "foods" in user_message:
        response = "🍴 Some top foods to try in Dubai: Shawarma 🌯, Mandi 🍖, Luqaimat 🍯, and Stuffed Vine Leaves 🍃. Would you like street food or fine dining suggestions?"
    elif "thanks" in user_message or "thank you" in user_message:
        response = "😊 You’re very welcome! If you need help planning or exploring Dubai, I’m here anytime! 🌟"
    else:
        response = "🤖 I specialize in Dubai travel advice. Could you ask me about places to visit, restaurants, shopping, or how to get around the city?"

    context_memory[user_id] = user_message
    await update.message.reply_text(response)

if __name__ == '__main__':
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🚀 Dubai Guide AI bot is running...")
    application.run_polling()