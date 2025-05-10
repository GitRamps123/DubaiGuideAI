# Dubai Guide AI Bot with Memory Upgrade
import os
import telebot
import openai

bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
openai.api_key = os.getenv("OPENAI_API_KEY")
conversation_history = {}

def get_chat_response(chat_id, user_input):
    history = conversation_history.get(chat_id, [])
    prompt = "\n".join(history + [f"User: {user_input}", "Bot:"])
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    answer = response.choices[0].message.content.strip()
    conversation_history[chat_id] = (history + [f"User: {user_input}", f"Bot: {answer}"])[-10:]
    return answer

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = get_chat_response(message.chat.id, message.text)
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, "Sorry, something went wrong.")

bot.infinity_polling()
