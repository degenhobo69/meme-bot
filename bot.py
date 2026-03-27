import requests
import time
import os
from telegram import Bot
from openai import OpenAI

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

def get_memes():
    url = "https://www.reddit.com/r/memes/top.json?limit=5&t=day"
    headers = {"User-agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    data = res.json()

    posts = []
    for p in data["data"]["children"]:
        title = p["data"]["title"]
        link = "https://reddit.com" + p["data"]["permalink"]
        posts.append(f"{title}\n{link}")

    return posts

def analyze(text):
    prompt = f"""
    Rate this meme for viral potential (1-10)
    and rewrite it to be funnier.

    Text: {text}

    Format:
    SCORE: X
    CAPTION: ...
    """

    res = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    reply = res.choices[0].message.content

    try:
        score = int(reply.split("SCORE:")[1].split("\n")[0])
        caption = reply.split("CAPTION:")[1].strip()
    except:
        score = 5
        caption = text

    return score, caption

def run():
    posts = get_memes()

    for p in posts:
        score, caption = analyze(p)

        if score >= 7:
            bot.send_message(
                chat_id=CHAT_ID,
                text=f"🔥 {caption}\n\n{p}"
            )
            time.sleep(2)

while True:
    run()
    time.sleep(1800)
