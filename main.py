import telebot
import requests
import logging

# Setup Logging taaki Render par error dikhe
logging.basicConfig(level=logging.INFO)

# --- CONFIGURATION ---
BOT_TOKEN = "7724762942:AAG5fMig2190WDTyqzqfPugxmyBN-QW3XK4"
OMDB_API_KEY = "378f0eb1"
# ---------------------

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 Welcome to MovieMintBot!\n\n"
        "Kisi bhi movie ka naam likhein aur main uski details nikaal kar doonga.\n"
        "Powered by: @viralmovies_hd"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def search_movie(message):
    movie_name = message.text
    print(f"Searching for: {movie_name}") # Logs mein dikhega
    
    # OMDB API Call
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={OMDB_API_KEY}"
    
    try:
        response = requests.get(url).json()
        
        if response.get("Response") == "True":
            title = response.get("Title")
            year = response.get("Year")
            rating = response.get("imdbRating")
            plot = response.get("Plot")
            poster = response.get("Poster")
            
            caption = (
                f"🎬 *{title}* ({year})\n\n"
                f"⭐ *Rating:* {rating}/10\n"
                f"📝 *Plot:* {plot}\n\n"
                f"📢 Join: @viralmovies_hd"
            )
            
            if poster and poster != "N/A":
                bot.send_photo(message.chat.id, poster, caption=caption, parse_mode="Markdown")
            else:
                bot.reply_to(message, caption, parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ Maaf kijiye, ye movie nahi mili!")
            
    except Exception as e:
        logging.error(f"Error: {e}")
        bot.reply_to(message, "⚠️ Kuch error aaya hai, baad mein try karein.")

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
