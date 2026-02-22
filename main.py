import os, telebot
from flask import Flask
from threading import Thread

# تنظیمات اصلی
BOT_TOKEN = "8335322668:AAF5Nhwo60k6NDPjU_KgTskcPU4A-UvRiaw"
ALLOWED_ADMINS = ['OYB1234', 'sahar143']
REACTIONS = ['⚡', '❤️‍🔥', '💯']
current_index = 0

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Bot is Alive!", 200

# --- اصلاح خط ۲۴: لیست کامل انواع محتوا برای ری‌اکت زدن ---
ALL_TYPES =

@bot.channel_post_handler(content_types=ALL_TYPES)
@bot.message_handler(content_types=ALL_TYPES)
def handle_messages(message):
    global current_index
    try:
        user = message.from_user.username if message.from_user else None
        is_admin = user and user.lower() in [admin.lower() for admin in ALLOWED_ADMINS]
        
        # ری‌اکت در کانال یا برای ادمین‌های لیست شده
        if message.chat.type == 'channel' or is_admin:
            bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[telebot.types.ReactionTypeEmoji(REACTIONS[current_index])]
            )
            current_index = (current_index + 1) % len(REACTIONS)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    # رفع مشکل Conflict (تداخل) با نسخه‌های قبلی
    bot.remove_webhook()
    
    # اجرای وب‌سرور روی پورت رندر
    port = int(os.environ.get("PORT", 10000))
    Thread(target=lambda: app.run(host='0.0.0.0', port=port)).start()
    
    # شروع کار ربات
    print("🚀 Robot is monitoring EVERYTHING now!")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
