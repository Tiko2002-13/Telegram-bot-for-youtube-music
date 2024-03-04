import os
import telebot
import yt_dlp as youtube_dl
from urllib.parse import urlparse, parse_qs
import os

# Set up your bot token
TOKEN = "6647245047:AAG0Eb4KocIlUUY4cJcJUVxp--JNP9uM8MA"
bot = telebot.TeleBot(TOKEN)

# Handler for the '/start' command
@bot.message_handler(commands=['start'])
def shoot(message):
    bot.send_message(message.chat.id, "Give me a YouTube link")

# Handler for all other messages
@bot.message_handler(func=lambda message: True)
def run(message):
    youtube_link = message.text

    # Check if it's a full YouTube link or a short link (youtu.be)
    parsed_url = urlparse(youtube_link)
    if parsed_url.netloc == 'youtu.be':
        video_id = parsed_url.path[1:]
        youtube_link = f'https://www.youtube.com/watch?v={video_id}'

    if "https://www.youtube.com" not in youtube_link:
        print("This is not a YouTube link!")
        bot.send_message(message.chat.id, "Please provide a valid YouTube link.")
        return

    bot.send_message(message.chat.id, "Please wait...")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(youtube_link, download=True)
            filename = ydl.prepare_filename(info_dict)

        print("Download complete... {}".format(filename))
        bot.send_audio(message.chat.id, audio=open(filename, 'rb'))

        # Delete the downloaded file
        os.remove(filename)

    except youtube_dl.utils.DownloadError as e:
        print("Error: Unable to download the video.")
        print("Download error:", e)
        bot.send_message(message.chat.id, "Sorry, I couldn't download the video from the provided link.")
    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, "An error occurred while processing the request.")

# Entry point for running the bot
def main():
    bot.polling()

if __name__ == "__main__":
    main()
