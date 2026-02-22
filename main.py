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
    return "Bot is Running!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# لیست کامل تمام محتواها (این بخش در کد شما خالی بود)
ALL_TYPES =

# هندلر برای کانال و گروه‌ها
@bot.channel_post_handler(content_types=ALL_TYPES)
@bot.message_handler(content_types=ALL_TYPES, func=lambda message: True)
def handle_all_messages(message):
    global current_index
    try:
        user = message.from_user.username if message.from_user else None
        is_admin = user and user.lower() in [admin.lower() for admin in ALLOWED_ADMINS]
        
        # اجرای ری‌اکشن در کانال یا برای ادمین‌های مشخص شده
        if message.chat.type == 'channel' or is_admin:
            bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[telebot.types.ReactionTypeEmoji(REACTIONS[current_index])]
            )
            current_index = (current_index + 1) % len(REACTIONS)
            print(f"Done: {message.content_type}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()
    bot.infinity_polling()
