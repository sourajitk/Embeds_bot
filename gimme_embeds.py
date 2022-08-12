import os
from dotenv import load_dotenv
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)
from telegram import Update
import logging

load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

# Use variables derived from custom API methods.
updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher


def start(update: Update, context: CallbackContext):
    """
    This function sets up the /start action to let the user know the
    bot is alive and ready to go.
    """
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello")

def edit_text(text):
    """
    This function edits the text of the message, by replacing some 
    website URLs with their vx counterparts that support embeds.
    """
    # Declare our list of to-be-replaced and new URLs.
    list_of_urls = ["twitter.com/", "tiktok.com/"]

    # Setup conditionals.
    # For Twitter
    if list_of_urls[0] in text:
        new_url = text.replace("twitter", "vxtwitter")
    # For TikTok
    elif list_of_urls[1] in text:
        new_url = text.replace("tiktok", "vxtiktok")
    return new_url


def text_handler(update, context):
    """
    The primary handler that does all the replacement action through
    the API.
    """

    # Use variables derived from custom API methods.
    message = update.message.text
    reply = update.message.reply_text

    """
    Check if the text contains an hyperlink.
    If it does, extract the URL and pass it to the edit_text function.
    If it doesn't, send the entire text to edit_text.
    """
    if update.message.entities[0].url is None:
        reply(edit_text(message))
    else:
        url = update.message.entities[0].url
        reply(edit_text(url))


start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)
message_handler = MessageHandler(Filters.text, text_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
