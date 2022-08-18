"""
Embeds here we come!
"""
import os
import logging
import re
import sys
from threading import Thread
from dotenv import load_dotenv
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
)

load_dotenv()
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

# Use variables derived from custom API methods.
updater = Updater(token=os.getenv("BOT_TOKEN"), use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    """
    This function sets up the /start action to let the user know the
    bot is alive and ready to go.
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Hey there, I am alive! \
I convert social media links that sometimes fail to show an embed with the message body.",
    )


def source(update, context):
    """
    This function sends a message to the chat that wants the source
    for the bot.
    """
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="This bot is brought to you by \
the citizens of Big Chungus LLC.\n\nSource: https://github.com/sourajitk/Embeds_bot",
    )


def edit_text(text):
    """
    This function edits the text of the message, by replacing some
    website URLs with their *x counterparts that support embeds.
    """

    new_url = None

    # Setup conditionals.
    # For Twitter
    if re.search(r"(?P<url>twitter.com/(.*?)/[^\s]+)", text, re.IGNORECASE) and not (
        re.search(r"(?P<url>xtwitter.com[^\s]+)", text, re.IGNORECASE)
        or re.search(r"(?P<url>twitter.com/i/events/[^\s]+)", text, re.IGNORECASE)
    ):
        # Isolate the Twitter URL.
        twitter_url = str(
            re.search(
                r"(?P<url>([^\s]*?)twitter.com[^\s]+)", text, re.IGNORECASE
            ).group("url")
        )
        insensitive_twitter = re.compile(re.escape("twitter.com"), re.IGNORECASE)
        new_url = insensitive_twitter.sub("vxtwitter.com", twitter_url)
        new_url = new_url.split("?")[0]  # Remove trackers

    # For TikTok
    elif re.search(
        r"(?P<url>tiktok.com/[^\s]+)", text, re.IGNORECASE
    ) and not re.search(r"(?P<url>xtiktok.com[^\s]+)", text, re.IGNORECASE):
        # Isolate the tiktok URL.
        tiktok_url = str(
            re.search(r"(?P<url>([^\s]*?)tiktok[^\s]+)", text, re.IGNORECASE).group(
                "url"
            )
        )
        insensitive_tiktok = re.compile(re.escape("tiktok.com"), re.IGNORECASE)
        new_url = insensitive_tiktok.sub("vxtiktok.com", tiktok_url)

    return new_url


def text_handler(update, context):  # pylint: disable=unused-argument
    """
    The primary handler that does all the replacement action through
    the API.
    """

    # Use variables derived from custom API methods.
    message = update.message.text
    reply = update.message.reply_text

    # Check if the text contains an hyperlink and if isn't None.
    # If it contains an hyperlink, extract the URL and pass it to edit_text.
    # If it doesn't, send the entire text to edit_text.

    hyperlink_url = update.message.entities[0].url

    if hyperlink_url is None:
        reply_url = edit_text(message)
        if reply_url is not None:
            reply(reply_url)
    else:
        reply_url = edit_text(hyperlink_url)
        if reply_url is not None:
            reply(reply_url)


def stop_and_restart():
    """
    Gracefully stop the Updater and replace the
    current process with a new one.
    """
    updater.stop()
    os.execl(sys.executable, sys.executable, *sys.argv)


def restart(update, context):  # pylint: disable=unused-argument
    """
    Allows whitelisted user_ids to restart the bot.
    """
    user_ids = [415397712, 177699182]
    filters = update.effective_user.id

    if filters in user_ids:
        update.message.reply_text("Bot is restarting...")
        Thread(target=stop_and_restart).start()
    else:
        update.message.reply_text(
            "Sorry, restarting the bot is restricted to its owners."
        )


# Handle the /start command.
start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)
# Handle the /source command.
source_handler = CommandHandler("source", source)
dispatcher.add_handler(source_handler)
# Main handler for links and hyperlinks.
message_handler = MessageHandler(
    (Filters.entity("url") | Filters.entity("text_link")), text_handler
)
dispatcher.add_handler(message_handler)
# Handler to stop the bot
dispatcher.add_handler(CommandHandler("r", restart))

updater.start_polling()
