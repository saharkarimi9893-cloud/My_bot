import os
import telebot
from flask import Flask, request

# تنظیمات (توکن و آدرس خود را چک کنید)
BOT_TOKEN = "8335322668:AAF5Nhwo60k6NDPjU_KgTskcPU4A-UvRiaw"
RENDER_URL = "https://my-bot-hrqm.onrender.com"

# نکته: threaded=False برای پایداری در پلن رایگان رندر
bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

ALLOWED_ADMINS = ['sahar143', 'OYB1234']
REACTIONS = ['⚡', '❤️‍🔥', '💯', '🔥', '💎']
current_index = 0
ALL_TYPES =

@app.route('/')
def home(): return "Bot is Alive!", 200

# مسیر ایمن برای وب‌هوک
@app.route('/webhook', methods=['POST'])
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
        if message.chat.type == 'channel' or is_admin:
            bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[telebot.types.ReactionTypeEmoji(REACTIONS[current_index])]
            )
            current_index = (current_index + 1) % len(REACTIONS)
    except Exception as e: print(f"Error: {e}")

if __name__ == '__main__':
    # ریست کردن وب‌هوک برای اطمینان
    bot.remove_webhook()
    # آدرس وب‌هوک باید دقیقا به /webhook ختم شود
    bot.set_webhook(url=f"{RENDER_URL}/webhook")
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
