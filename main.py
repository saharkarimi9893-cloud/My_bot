import os
import telebot
from flask import Flask
from threading import Thread

# تنظیمات ربات
BOT_TOKEN = "8335322668:AAF5Nhwo60k6NDPjU_KgTskcPU4A-UvRiaw"
ALLOWED_ADMINS = ['OYB1234', 'sahar143']
REACTIONS = ['⚡', '❤️‍🔥', '💯']
current_index = 0

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Active!", 200

def run_flask():
    # استفاده از پورت محیطی رندر
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# لیست کامل تمام محتواها (رفع خطای خط 24 تصویر)
ALL_TYPES =

# هندلر برای کانال و گروه‌ها با پوشش تمام محتواها
@bot.channel_post_handler(content_types=ALL_TYPES)
@bot.message_handler(content_types=ALL_TYPES, func=lambda message: True)
def handle_all_messages(message):
    global current_index
    try:
        user = message.from_user.username if message.from_user else None
        is_admin = user and user.lower() in [admin.lower() for admin in ALLOWED_ADMINS]
        
        # ری‌اکت روی پست کانال یا پیام ادمین در گروه
        if message.chat.type == 'channel' or is_admin:
            bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[telebot.types.ReactionTypeEmoji(REACTIONS[current_index])]
            )
            current_index = (current_index + 1) % len(REACTIONS)
            print(f"✅ Reacted to {message.content_type}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    # اجرای همزمان سرور و ربات
    Thread(target=run_flask, daemon=True).start()
    print("🚀 Robot is monitoring EVERYTHING...")
    bot.infinity_polling()
