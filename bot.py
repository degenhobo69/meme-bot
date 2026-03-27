print("NEW VERSION RUNNING")

import os
import requests
import asyncio
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
        print("Error fetching memes:", e)
        return []

async def run():
    while True:
        try:
            memes = get_memes()

            for meme in memes[:5]:
                try:
                    await bot.send_message(
                        chat_id=CHAT_ID,
                        text=f"😂 {meme}"
                    )
                    await asyncio.sleep(2)
                except Exception as e:
                    print("Send error:", e)

            await asyncio.sleep(120)  # 2 minutes

        except Exception as e:
            print("Main loop error:", e)
            await asyncio.sleep(30)

asyncio.run(run())
