import os
import telebot
from flask import Flask
from threading import Thread

# توکن ربات شما
BOT_TOKEN = "8335322668:AAF5Nhwo60k6NDPjU_KgTskcPU4A-UvRiaw"

# ادمین‌های مجاز (برای گروه‌ها و پی‌وی)
ALLOWED_ADMINS = ['OYB1234', 'sahar143']

# لیست ری‌اکشن‌ها
REACTIONS = ['⚡', '❤️‍🔥', '💯']
current_index = 0

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Active for Channels and Groups!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# این هندلر مخصوص پست‌های کانال است
@bot.channel_post_handler(func=lambda message: True)
# این هندلر مخصوص پیام‌های گروه و پی‌وی است
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    global current_index
    try:
        # چک کردن ادمین بودن در گروه‌ها
        is_admin = False
        if message.from_user and message.from_user.username:
            if message.from_user.username.lower() in [admin.lower() for admin in ALLOWED_ADMINS]:
                is_admin = True
        
        # اگر پست در کانال بود یا ادمین در گروه پیام داد:
        if message.chat.type == 'channel' or is_admin:
            bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[telebot.types.ReactionTypeEmoji(REACTIONS[current_index])]
            )
            # رفتن به ری‌اکشن بعدی
            current_index = (current_index + 1) % len(REACTIONS)
            print(f"✅ Reaction sent in {message.chat.type}!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    # اجرای وب‌سرور برای زنده ماندن در رندر
    Thread(target=run_flask, daemon=True).start()
    
    print("🚀 Robot is Online and monitoring Channels/Groups...")
    bot.infinity_polling()
