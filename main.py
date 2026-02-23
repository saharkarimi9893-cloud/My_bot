import os
import telebot
from flask import Flask
from threading import Thread

# Config
BOT_TOKEN = "8335322668:AAF5Nhwo60k6NDPjU_KgTskcPU4A-UvRiaw"
ALLOWED_ADMINS = ['sahar143', 'OYB1234']
REACTIONS = ['⚡', '❤️‍🔥', '💯', '🔥', '💎']
current_index = 0

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "Bot is Alive!", 200

ALL_TYPES = ['text', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact']

@bot.channel_post_handler(content_types=ALL_TYPES)
@bot.message_handler(content_types=ALL_TYPES)
def handle_messages(message):
    global current_index
    try:
        user = message.from_user.username if message.from_user else None
        # Check if message is from a channel OR from one of your admins
        is_admin = user and user.lower() in [admin.lower() for admin in ALLOWED_ADMINS]
        
        if message.chat.type == 'channel' or is_admin:
            bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[telebot.types.ReactionTypeEmoji(REACTIONS[current_index])]
            )
            current_index = (current_index + 1) % len(REACTIONS)
    except Exception as e:
        print(f"Error: {e}")

def run():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    Thread(target=run).start()
    bot.remove_webhook()
    print("🚀 Running with Admins: sahar143 & OYB1234")
    bot.infinity_polling()
