import asyncio
import os
from flask import Flask
from threading import Thread
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji

# --- تنظیمات شما (بر اساس تصویر) ---
API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
BOT_TOKEN = "8335322668:AAFFUKKmKzAOrbPz9bhl1wEjy48SCxaI0Eg"
ALLOWED_ADMINS = ['OYB1234', 'sahar143']
REACTIONS = ['⚡', '❤️‍🔥', '💯']
current_index = 0

# --- وب‌سرور برای بیدار ماندن در رندر ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running!", 200

def run_flask():
    # رندر پورت را خودش تعیین می‌کند
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- منطق اصلی ربات ---
# استفاده از سشن مموری برای جلوگیری از خطای دیتابیس در رندر
client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    global current_index
    try:
        sender = await event.get_sender()
        if sender and hasattr(sender, 'username') and sender.username in ALLOWED_ADMINS:
            # ارسال ریکوئست با await (حیاتی)
            await client(SendReactionRequest(
                peer=event.chat_id, 
                msg_id=event.id,
                reaction=[ReactionEmoji(emoticon=REACTIONS[current_index])]
            ))
            current_index = (current_index + 1) % len(REACTIONS)
    except Exception as e:
        print(f"Error: {e}")

async def main():
    # ۱. اجرای وب‌سرور در پس‌زمینه
    Thread(target=run_flask, daemon=True).start()
    
    # ۲. شروع به کار ربات
    await client.start(bot_token=BOT_TOKEN)
    print("🚀 Robot is online on Render!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
