import asyncio
import os
import requests
import time
from flask import Flask
from threading import Thread
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji

# تنظیمات خودکار
API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
BOT_TOKEN = "8335322668:AAFFUKKmKzAOrbPz9bhl1wEjy48SCxaI0Eg"
ALLOWED_ADMINS = ['OYB1234', 'sahar143']
REACTIONS = ['⚡', '❤️‍🔥', '💯']
current_index = 0
APP_URL = "https://my-bot-hrqm.onrender.com"

# وب‌سرور برای زنده ماندن در رندر
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Online!"

def run_flask():
    # پورت ۱۰۰۰۰ پورت استاندارد رندر است
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    while True:
        try:
            time.sleep(600)
            requests.get(APP_URL)
            print("Self-ping: I am awake!")
        except: pass

client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    global current_index
    sender = await event.get_sender()
    if sender and sender.username in ALLOWED_ADMINS:
        try:
            await client(SendReactionRequest(
                peer=event.chat_id, msg_id=event.id,
                reaction=[ReactionEmoji(emoticon=REACTIONS[current_index])]
            ))
            current_index = (current_index + 1) % len(REACTIONS)
        except: pass

async def main():
    Thread(target=run_flask, daemon=True).start()
    Thread(target=keep_alive, daemon=True).start()
    await client.start(bot_token=BOT_TOKEN)
    print("🚀 Robot is online and permanent!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
