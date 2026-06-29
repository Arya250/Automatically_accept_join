import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ChatJoinRequestHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ================= CONFIG =================

BOT_TOKEN = "8885525564:AAFxEU7JH5bs_y_FuYBGg1oubrKi4cxKCwU"

# Pehle temporary yahan koi image mat dalo
WELCOME_IMAGE = "AgACAgUAAxkBAANzai6VD1B05CQf-eU-Qlsp8mPAxqoAAr0QaxsGxXBVSKQqSfzSkcQBAAMCAAN4AAM8BA"

THANKS_IMAGE = "AgACAgUAAxkBAAN0ai6VD9SaCPVMQg8O7cb3_uuc4wQAAh0RaxvSK3hVvAhFc5r1KPABAAMCAAN4AAM8BA"

CHANNEL_LINK = "https://t.me/premium_vedioss"


# ================= LOGGING =================

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


# ================= FILE ID GETTER =================

async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        file_id = update.message.photo[-1].file_id

        await update.message.reply_text(
            f"📌 Your File ID:\n\n{file_id}"
        )


# ================= AUTO APPROVE =================

async def auto_accept(update: Update, context: ContextTypes.DEFAULT_TYPE):

    request = update.chat_join_request
    user = request.from_user

    try:
        await context.bot.approve_chat_join_request(
            request.chat.id,
            user.id
        )

        button = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📢 Join Channel",
                    url=CHANNEL_LINK
                )
            ]
        ])

        if THANKS_IMAGE:
            await context.bot.send_photo(
                chat_id=user.id,
                photo=THANKS_IMAGE,
                caption=f"""🔥 Welcome {user.first_name} 🎉

✅ Your join request has approved!
🌟 Thanks for joining our community.
📢 Stay active and enjoy our content.
🚀 Have a great day!""",
                reply_markup=button
            )
        else:
            await context.bot.send_message(
                chat_id=user.id,
                text=f"""🔥 Welcome {user.first_name} 🎉

✅ Your join request has approved!
🌟 Thanks for joining our community.
📢 Stay active and enjoy our content.
🚀 Have a great day!""",
                reply_markup=button
            )

    except Exception as e:
        logging.error(f"Auto approve error: {e}")


# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:
        if WELCOME_IMAGE:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=WELCOME_IMAGE,
                caption="""🔥 Welcome to Auto Join System Bot!

🤖 Your bot is now ACTIVE
⚡ Auto join request approval enabled
🚀 Just add me admin in your channel !"""
            )
        else:
            await update.message.reply_text(
                """🔥 Welcome to Auto Join System Bot!

🤖 Your bot is now ACTIVE
⚡ Auto join request approval enabled
🚀 Just add me admin in your channel !"""
            )

    except Exception as e:
        logging.error(f"Start error: {e}")


# ================= MAIN =================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        ChatJoinRequestHandler(auto_accept)
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    # Photo send karke File ID nikalne ke liye
    app.add_handler(
        MessageHandler(filters.PHOTO, get_file_id)
    )

    print("🤖 Auto Join Bot Running Successfully...")

    app.run_polling()


if __name__ == "__main__":
    main()
