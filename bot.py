import os
import time
import requests
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

def get_memes():
    url = "https://meme-api.com/gimme/5"

    try:
        res = requests.get(url, timeout=10)
        data = res.json()

        memes = []
        for post in data["memes"]:
            title = post["title"]
            link = post["url"]
            memes.append(f"{title}\n{link}")

        return memes

    except Exception as e:
        print("Error:", e)
        return []

def run():
    while True:
        memes = get_memes()

        for meme in memes:
            try:
                bot.send_message(
                    chat_id=CHAT_ID,
                    text=f"😂 {meme}"
                )
                time.sleep(3)
            except Exception as e:
                print("Send error:", e)

        time.sleep(1800)  # every 30 minutes

run()
