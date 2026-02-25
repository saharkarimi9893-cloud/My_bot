import os
import telebot
from flask import Flask, request

# تنظیمات نهایی با آدرس صحیح شما
BOT_TOKEN = "8335322668:AAF5Nhwo60k6NDPjU_KgTskcPU4A-UvRiaw"
RENDER_URL = "https://my-bot-hrqm.onrender.com" 

ALLOWED_ADMINS = ['sahar143', 'OYB1234']
REACTIONS = ['⚡', '❤️‍🔥', '💯', '🔥',]
current_index = 0

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# لیست کامل محتواها طبق درخواست شما
ALL_TYPES = ['photo', 'video', 'sticker', 'audio', 'animation', 'text', 'voice', 'story', 'video_note']

@app.route('/')
def home(): 
    return "Bot is Active!", 200

@app.route('/' + BOT_TOKEN, methods=['POST'])
def get_message():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    return "Forbidden", 403

@bot.channel_post_handler(content_types=ALL_TYPES)
@bot.message_handler(content_types=ALL_TYPES)
def handle_messages(message):
    global current_index
    try:
        user = message.from_user.username if message.from_user else None
        is_admin = user and user.lower() in [admin.lower() for admin in ALLOWED_ADMINS]

        # ری‌اکشن روی تمام پست‌های کانال و ادمین‌ها
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
    # تنظیم وب‌هوک روی آدرس رندر
    bot.remove_webhook()
    bot.set_webhook(url=RENDER_URL + '/' + BOT_TOKEN)
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
