import telebot
import requests
import time

# 1. Apna Telegram Token yahan dalein
BOT_TOKEN = "7724762942:AAG5fMig2190WDTyqzqfPugxmyBN-QW3XK4"

bot = telebot.TeleBot(BOT_TOKEN)

# Purane connections khatam karne ke liye
bot.remove_webhook()
time.sleep(1)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "🎬 Welcome to MovieMintBot!\n\nKisi bhi Movie ya Web Series ka naam likho, main TVMaze se details nikalunga.\n\nJoin: @viralmovies_hd")

@bot.message_handler(func=lambda message: True)
def get_tv_show_details(message):
    query = message.text
    # TVMaze API - No Key Required
    url = f"https://api.tvmaze.com/singlesearch/shows?q={query}"
    
    try:
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            
            name = data.get('name', 'N/A')
            rating = data.get('rating', {}).get('average', 'N/A')
            # HTML tags saaf karne ke liye
            summary = data.get('summary', 'No summary available.').replace('<p>', '').replace('</p>', '').replace('<b>', '').replace('</b>', '')
            genres = ", ".join(data.get('genres', []))
            image = data.get('image', {}).get('original')
            
            caption = f"📺 *{name}*\n⭐ Rating: {rating}/10\n🎭 Genres: {genres}\n\n📝 *Summary:* {summary[:300]}...\n\n📥 Join: @viralmovies_hd"
            
            if image:
                bot.send_photo(message.chat.id, image, caption=caption, parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, caption, parse_mode="Markdown")
        else:
            bot.reply_to(message, "❌ Data nahi mila! Spelling check karein.")
            
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "⚠️ Server busy hai, baad mein try karein.")

print("Bot is starting...")
bot.infinity_polling()
