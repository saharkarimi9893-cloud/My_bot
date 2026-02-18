import asyncio
import os
from flask import Flask
from threading import Thread
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji

# --- تنظیمات ---
API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
BOT_TOKEN = "8335322668:AAFFUKKmKzAOrbPz9bhl1wEjy48SCxaI0Eg"
ALLOWED_ADMINS = ['OYB1234', 'sahar143'] 
REACTIONS = ['⚡', '❤️‍🔥', '💯']
current_index = 0 

# --- ترفند زنده نگه داشتن در رندر (Flask) ---
app = Flask(__name__)
@app.route('/')
def home(): return "Bot is Alive!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- منطق ربات ---
client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    global current_index
    sender = await event.get_sender()
    # بررسی دقیق یوزرنیم ادمین
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
            print(f"⚠️ Error: {e}")

async def main():
    # اجرای وب‌سرور در پس‌زمینه
    Thread(target=run_flask, daemon=True).start()
    
    await client.start(bot_token=BOT_TOKEN)
    print("🚀 Robot is online!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
