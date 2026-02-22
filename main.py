import os
import telebot
from flask import Flask
from threading import Thread

# توکن ربات شما
BOT_TOKEN = "8335322668:AAF5Nhwo60k6NDPjU_KgTskcPU4A-UvRiaw"

# ادمین‌های مجاز
ALLOWED_ADMINS = ['OYB1234', 'sahar143']

# لیست ری‌اکشن‌ها
REACTIONS = ['⚡', '❤️‍🔥', '💯']
current_index = 0

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive for All Content Types!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# این بخش بسیار مهم است: اضافه کردن تمام content_types
@bot.channel_post_handler(content_types=)
@bot.message_handler(content_types=)
def handle_all_messages(message):
    global current_index
    try:
        # بررسی ادمین بودن
        is_admin = False
        if message.from_user and message.from_user.username:
            if message.from_user.username.lower() in [admin.lower() for admin in ALLOWED_ADMINS]:
                is_admin = True
        
        # اگر پست در کانال بود یا ادمین پیام داد (با هر محتوایی)
        if message.chat.type == 'channel' or is_admin:
            bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[telebot.types.ReactionTypeEmoji(REACTIONS[current_index])]
            )
            # رفتن به ری‌اکشن بعدی
            current_index = (current_index + 1) % len(REACTIONS)
            print(f"✅ Reaction sent to {message.content_type} in {message.chat.type}!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    # اجرای وب‌سرور برای زنده ماندن
    Thread(target=run_flask, daemon=True).start()
    
    print("🚀 Robot is monitoring ALL content types...")
    bot.infinity_polling()
