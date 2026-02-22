import os
import telebot
from flask import Flask
from threading import Thread

# توکن ربات شما
BOT_TOKEN = "8335322668:AAF5Nhwo60k6NDPjU_KgTskcPU4A-UvRiaw"
ALLOWED_ADMINS = ['OYB1234', 'sahar143']
REACTIONS = ['⚡', '❤️‍🔥', '💯']
current_index = 0

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive for ALL Content Types!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# لیست تمام انواع محتوا که ربات باید ببیند
ALL_CONTENT_TYPES =

# هندلر مخصوص کانال و گروه برای تمام فایل‌ها
@bot.channel_post_handler(content_types=ALL_CONTENT_TYPES)
@bot.message_handler(content_types=ALL_CONTENT_TYPES)
def handle_all_messages(message):
    global current_index
    try:
        # تشخیص ادمین (در پی‌وی و گروه)
        user = message.from_user.username if message.from_user else None
        is_admin = user and user.lower() in [admin.lower() for admin in ALLOWED_ADMINS]
        
        # اگر پست در کانال بود یا ادمین پیام (هر محتوایی) فرستاد:
        if message.chat.type == 'channel' or is_admin:
            bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[telebot.types.ReactionTypeEmoji(REACTIONS[current_index])]
            )
            current_index = (current_index + 1) % len(REACTIONS)
            print(f"✅ Reaction sent to {message.content_type}!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    Thread(target=run_flask, daemon=True).start()
    print("🚀 Robot is monitoring EVERYTHING now!")
    bot.infinity_polling()
