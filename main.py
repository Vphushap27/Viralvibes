import telebot
import requests
import time

# Tokens
BOT_TOKEN = "7724762942:AAG5fMig2190WDTyqzqfPugxmyBN-QW3XK4"
OMDB_API_KEY = "378f0eb1" 

bot = telebot.TeleBot(BOT_TOKEN)

# --- WEBHOOK ERROR FIX ---
# Ye line purane kisi bhi connection ko khatam kar degi
bot.remove_webhook()
time.sleep(1) 
# -------------------------

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🎬 Welcome to MovieMintBot!\n\nMovie ka naam likho, main details nikalunga.\nJoin: @viralmovies_hd")

@bot.message_handler(func=lambda message: True)
def get_movie_details(message):
    movie_name = message.text
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    try:
        response = requests.get(url).json()
        if response.get('Response') == "True":
            title = response['Title']
            year = response['Year']
            rating = response['imdbRating']
            poster = response['Poster']
            caption = f"🎬 *{title} ({year})*\n⭐ IMDb: {rating}/10\n\n📥 Download: @viralmovies_hd"
            if poster != "N/A":
                bot.send_photo(message.chat.id, poster, caption=caption, parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, caption, parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ Movie nahi mili!")
    except Exception as e:
        print(f"Error: {e}")

print("Bot is starting...")
bot.infinity_polling() # Infinity polling zyada stable hoti hai
