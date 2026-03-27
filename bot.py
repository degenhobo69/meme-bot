import os
import time
from telegram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

def run():
    while True:
        try:
            bot.send_message(
                chat_id=CHAT_ID,
                text="🔥 Bot is alive and working!"
            )
            time.sleep(60)  # every 1 minute

        except Exception as e:
            print("Error:", e)
            time.sleep(10)

run()
