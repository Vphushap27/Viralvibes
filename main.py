import telebot
import requests
import os
from flask import Flask
from threading import Thread

# 1. Dummy Flask Server (Port error fix karne ke liye)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    # Render automatically 'PORT' environment variable deta hai
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# 2. Bot Setup
BOT_TOKEN = "7724762942:AAG5fMig2190WDTyqzqfPugxmyBN-QW3XK4"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🎬 Welcome! Main live hoon.\nJoin: @viralmovies_hd")

@bot.message_handler(func=lambda message: True)
def get_details(message):
    query = message.text
    url = f"https://api.tvmaze.com/singlesearch/shows?q={query}"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            name = data.get('name')
            image = data.get('image', {}).get('original')
            caption = f"📺 *{name}*\n\n📥 Join: @viralmovies_hd"
            if image:
                bot.send_photo(message.chat.id, image, caption=caption, parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, caption, parse_mode="Markdown")
    except Exception as e:
        print(f"Error: {e}")

# 3. Dono ko saath chalana
if __name__ == "__main__":
    # Server ko background mein start karo
    t = Thread(target=run)
    t.start()
    
    # Bot ko start karo
    print("Bot is starting...")
    bot.infinity_polling()

bot.infinity_polling(timeout=10, long_polling_timeout=5)
