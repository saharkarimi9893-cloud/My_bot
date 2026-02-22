import os
import telebot
from flask import Flask
from threading import Thread

# دریافت توکن از تنظیمات رندر (Environment Variables)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# لیست ادمین‌های مجاز (یوزرنیم بدون @)
ALLOWED_ADMINS = ['OYB1234', 'sahar143']

# لیست ری‌اکشن‌ها برای چرخش خودکار
REACTIONS = ['⚡', '❤️‍🔥', '💯']
current_index = 0

# راه‌اندازی ربات
bot = telebot.TeleBot(BOT_TOKEN)

# ساخت یک وب‌سرور ساده برای آنلاین نگه داشتن ربات در رندر
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive and Running!", 200

def run_flask():
    # رندر پورت را خودکار اختصاص می‌دهد
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# هندلر برای شناسایی پیام‌های جدید و زدن ری‌اکشن
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    global current_index
    try:
        # چک کردن اینکه فرستنده پیام ادمین است یا خیر
        if message.from_user and message.from_user.username in ALLOWED_ADMINS:
            # ارسال ری‌اکشن به پیام ادمین
            bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[telebot.types.ReactionTypeEmoji(REACTIONS[current_index])]
            )
            # تغییر ری‌اکشن برای پیام بعدی
            current_index = (current_index + 1) % len(REACTIONS)
            print(f"Reaction {REACTIONS[current_index-1]} sent successfully!")
    except Exception as e:
        print(f"Error in reaction: {e}")

if __name__ == '__main__':
    # ۱. اجرای وب‌سرور در یک رشته (Thread) جداگانه
    Thread(target=run_flask, daemon=True).start()
    
    # ۲. اجرای اصلی ربات
    print("🚀 Robot is Online and waiting for messages...")
    bot.infinity_polling()
