import os
import telebot
from flask import Flask, request

# تنظیمات اصلی
BOT_TOKEN = "8335322668:AAF5Nhwo60k6NDPjU_KgTskcPU4A-UvRiaw"
RENDER_URL = "https://your-app-name.onrender.com" # آدرس رندر خود را اینجا بزنید

ALLOWED_ADMINS = ['sahar143', 'OYB1234']
REACTIONS = ['⚡', '❤️‍🔥', '💯', '🔥', '💎']
current_index = 0

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Bot is Alive!", 200

@app.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# لیست کامل انواع محتوا برای واکنش به همه چیز
ALL_TYPES =

@bot.channel_post_handler(content_types=ALL_TYPES)
@bot.message_handler(content_types=ALL_TYPES)
def handle_messages(message):
    global current_index
    try:
        # اگر پیام در کانال بود یا فرستنده ادمین بود
        user = message.from_user.username if message.from_user else None
        is_admin = user and user.lower() in [admin.lower() for admin in ALLOWED_ADMINS]

        if message.chat.type == 'channel' or is_admin:
            bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[telebot.types.ReactionTypeEmoji(REACTIONS[current_index])]
            )
            # تغییر ری‌اکشن برای پیام بعدی
            current_index = (current_index + 1) % len(REACTIONS)
    except Exception as e:
        print(f"Error reacting: {e}")

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + '/' + BOT_TOKEN)
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
