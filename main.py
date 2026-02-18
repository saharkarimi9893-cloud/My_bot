import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji

# --- تنظیمات اختصاصی شما ---
API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"
BOT_TOKEN = "8335322668:AAFFUKKmKzAOrbPz9bhl1wEjy48SCxaI0Eg"

# لیست یوزرنیم ادمین‌ها (بدون @)
ALLOWED_ADMINS = ['OYB1234', 'sahar143'] 
REACTIONS = ['⚡', '❤️‍🔥', '💯']
current_index = 0 

# در Render نیازی به پروکسی نیست، اتصال مستقیم است
client = TelegramClient('bot_session', API_ID, API_HASH)

@client.on(events.NewMessage)
async def handler(event):
    global current_index
    
    # بررسی اینکه آیا پیام از طرف ادمین مجاز است یا در گروه/کانالی که ادمین در آن هست
    sender = await event.get_sender()
    if sender and sender.username in ALLOWED_ADMINS:
        if event.is_channel or event.is_group:
            try:
                selected_emoji = REACTIONS[current_index]
                # وقفه کوتاه برای طبیعی به نظر رسیدن
                await asyncio.sleep(2) 
                
                await client(SendReactionRequest(
                    peer=event.chat_id,
                    msg_id=event.id,
                    reaction=[ReactionEmoji(emoticon=selected_emoji)]
                ))
                print(f"✅ ری‌اکشن '{selected_emoji}' توسط ادمین ثبت شد.")
                current_index = (current_index + 1) % len(REACTIONS)
            except Exception as e:
                print(f"⚠️ خطا: {e}")

async def main():
    try:
        await client.start(bot_token=BOT_TOKEN)
        print("🚀 ربات در Render با موفقیت روشن شد و آماده کار است.")
        await client.run_until_disconnected()
    except Exception as e:
        print(f"❌ خطای اتصال کلی: {e}")

if __name__ == '__main__':
    # اجرای اصلی ربات
    asyncio.run(main())
