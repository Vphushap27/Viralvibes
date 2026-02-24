import telebot
import requests
import logging
from flask import Flask
from threading import Thread

# 1. Flask App Setup (Render ko port dene ke liye)
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    # Render default port 10000 use karta hai
    app.run(host='0.0.0.0', port=10000)

# 2. Telegram Bot Setup
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = "7724762942:AAG5fMig2190WDTyqzqfPugxmyBN-QW3XK4"
OMDB_API_KEY = "378f0eb1"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎬 Welcome to MovieMintBot!\nMovie ka naam likhein details ke liye.\nPowered by: @viralmovies_hd")

@bot.message_handler(func=lambda message: True)
def search_movie(message):
    movie_name = message.text
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    
    try:
        response = requests.get(url).json()
        if response.get("Response") == "True":
            title = response.get("Title")
            year = response.get("Year")
            rating = response.get("imdbRating")
            plot = response.get("Plot")
            poster = response.get("Poster")
            
            # HTML parse mode use kar rahe hain taaki symbols error na dein
            caption = (
                f"🎬 <b>{title}</b> ({year})\n\n"
                f"⭐ <b>Rating:</b> {rating}/10\n"
                f"📝 <b>Plot:</b> {plot}\n\n"
                f"📢 Join: @viralmovies_hd"
            )
            
            if poster and poster != "N/A":
                bot.send_photo(message.chat.id, poster, caption=caption, parse_mode="HTML")
            else:
                bot.reply_to(message, caption, parse_mode="HTML")
        else:
            bot.reply_to(message, "❌ Movie nahi mili!")
    except Exception as e:
        logging.error(f"Error: {e}")

# 3. Dono ko saath chalane ke liye Threading
if __name__ == "__main__":
    # Flask ko background mein start karein
    t = Thread(target=run_flask)
    t.start()
    
    print("Bot is starting...")
    bot.infinity_polling()
