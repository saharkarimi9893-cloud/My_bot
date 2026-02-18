import asyncio
import os
import requests
import time
from flask import Flask
from threading import Thread
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji

# --- تنظیمات اختصاصی ---
# از متغیرهای محیطی که در پنل رندر تنظیم کردید استفاده می‌کنیم
API_ID = int(os.environ.get("API_ID", 2040))
API_HASH = os.environ.get("API_HASH", "b18441a1ff607e10a989891a5462e627")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8335322668:AAFFUKKmKzAOrbPz9bhl1wEjy48SCxaI0Eg")

ALLOWED_ADMINS = ['OYB1234', 'sahar143'] 
REACTIONS = ['⚡', '❤️‍🔥', '💯']
current_index = 0 

# آدرس وب‌سایت شما در رندر برای سیستم بیدارباش
APP_URL = "https://my-bot-hrqm.onrender.com"

# --- ۱. وب‌سرور برای زنده نگه داشتن (Flask) ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive and Running!"

def run_flask():
    # رندر پورت را به صورت خودکار تعیین می‌کند
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- ۲. سیستم بیدارباش خودکار (Self-Ping) ---
def keep_alive():
    while True:
        try:
            time.sleep(600) # هر ۱۰ دقیقه
            requests.get(APP_URL)
            print("Successfully pinged to stay awake.")
        except:
            pass

# --- ۳. منطق اصلی ربات تلگرام ---
client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    global current_index
    sender = await event.get_sender()
    
    # بررسی یوزرنیم ادمین (بدون @)
    if sender and sender.username in ALLOWED_ADMINS:
        try:
            selected_emoji = REACTIONS[current_index]
            await client(SendReactionRequest(
                peer=event.chat_id,
                msg_id=event.id,
                reaction=[ReactionEmoji(emoticon=selected_emoji)]
            ))
            current_index = (current_index + 1) % len(REACTIONS)
            print(f"✅ Reacted with {selected_emoji}")
        except Exception as e:
            print(f"⚠️ Reaction Error: {e}")

async def main():
    # اجرای وب‌سرور و بیدارباش در پس‌زمینه
    Thread(target=run_flask, daemon=True).start()
    Thread(target=keep_alive, daemon=True).start()
    
    await client.start(bot_token=BOT_TOKEN)
    print("🚀 Robot is online and permanent mode is active!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
