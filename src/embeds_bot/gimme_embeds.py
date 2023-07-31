"""Embeds here we come!"""
import os
import re
import sys
from threading import Thread


class GimmeEmbeds:
    """Class to handle the bot's actions."""
    def __init__(self, db): # pylint: disable=invalid-name
        self.db = db # pylint: disable=invalid-name

    def start(self, update, context):
        """
        This function sets up the /start action to let the user know the
        bot is alive and ready to go.
        """
        chat_id = update.effective_chat.id
        context.bot.send_message(
            chat_id,
            "Hey there, I am alive!\n"
            + "I convert social media links that sometimes fail to show"
            + "an embed with the message body.",
        )
        # Create a database for the chat.
        redis_db = self.db.create_db(chat_id)
        # Convert the database to a dictionary to store it locally, so the bot doesn't
        # have to query the database every time users send a link.
        self.filter_db = {  # pylint: disable=attribute-defined-outside-init
            k.decode("utf-8"): v.decode("utf-8") for k, v in redis_db.items()
        }

    def source(self, update, context):
        """
        This function sends a message to the chat that wants the source
        for the bot.
        """
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="This bot is brought to you by the citizens of Big Chungus LLC."
            + "\n\nSource: https://github.com/sourajitk/Embeds_bot",
        )

    def edit_text(self, text, chat_id):
        """
        This function edits the text of the message, by replacing some
        website URLs with their *x counterparts that support embeds.
        """

        new_url = None

        # try-catch AttributeError of filter_db, which is needed when the code is
        # manually stopped and restarted.
        try:
            database = self.filter_db
        except AttributeError:
            self.filter_db = self.db.get_db( # pylint: disable=attribute-defined-outside-init
                chat_id
            )
            database = self.filter_db

        # Setup conditionals.
        # For Twitter
        if (
            re.search(r"(?P<url>twitter.com/(.*?)/[^\s]+)", text, re.IGNORECASE)
            and not (
                re.search(r"(?P<url>xtwitter.com[^\s]+)", text, re.IGNORECASE)
                or re.search(
                    r"(?P<url>twitter.com/i/events/[^\s]+)", text, re.IGNORECASE
                )
                or re.search(
                    r"(?P<url>twitter.com/i/spaces/[^\s]+)", text, re.IGNORECASE
                )
            )
            and database["twitter"] == "1"
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
        elif (
            re.search(r"(?P<url>tiktok.com/[^\s]+)", text, re.IGNORECASE)
            and not re.search(r"(?P<url>xtiktok.com[^\s]+)", text, re.IGNORECASE)
            and database["tiktok"] == "1"
        ):
            # Isolate the tiktok URL.
            tiktok_url = str(
                re.search(r"(?P<url>([^\s]*?)tiktok[^\s]+)", text, re.IGNORECASE).group(
                    "url"
                )
            )
            insensitive_tiktok = re.compile(re.escape("tiktok.com"), re.IGNORECASE)
            new_url = insensitive_tiktok.sub("vxtiktok.com", tiktok_url)

        # For Instagram
        elif (
            re.search(r"(?P<url>instagram.com/[^\s]+)", text, re.IGNORECASE)
            and not re.search(r"(?P<url>ddinstagram.com[^\s]+)", text, re.IGNORECASE)
            and database["instagram"] == "1"
        ):
            # Isolate the Instagram URL.
            instagram_url = str(
                re.search(
                    r"(?P<url>([^\s]*?)instagram[^\s]+)", text, re.IGNORECASE
                ).group("url")
            )
            insensitive_instagram = re.compile(
                re.escape("instagram.com"), re.IGNORECASE
            )
            new_url = insensitive_instagram.sub("ddinstagram.com", instagram_url)
            new_url = new_url.split("/?")[0]

        # For Bluesky
        elif re.search(
            r"(?P<url>bsky.app/[^\s]+)", text, re.IGNORECASE
        ) and not re.search(r"(?P<url>psky.app[^\s]+)", text, re.IGNORECASE):
            # Isolate the bsky URL.
            bsky_url = str(
                re.search(r"(?P<url>([^\s]*?)bsky[^\s]+)", text, re.IGNORECASE).group(
                    "url"
                )
            )
            insensitive_tiktok = re.compile(re.escape("bsky.app"), re.IGNORECASE)
            new_url = insensitive_tiktok.sub("psky.app", bsky_url)

        return new_url

    def text_handler(self, update, context):  # pylint: disable=unused-argument
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
            reply_url = self.edit_text(message, update.effective_chat.id)
            if reply_url is not None:
                reply(reply_url)
        else:
            reply_url = self.edit_text(hyperlink_url, update.effective_chat.id)
            if reply_url is not None:
                reply(reply_url)

    def stop_and_restart(self):
        """
        Gracefully stop the Updater and replace the
        current process with a new one.
        """
        self.updater.stop()  # pylint: disable=no-member
        os.execl(sys.executable, sys.executable, *sys.argv)

    def restart(self, update, context):  # pylint: disable=unused-argument
        """
        Allows whitelisted user_ids to restart the bot.
        """
        user_ids = [415397712, 177699182]
        filters = update.effective_user.id

        if filters in user_ids:
            update.message.reply_text("Bot is restarting...")
            Thread(target=self.stop_and_restart).start()
        else:
            update.message.reply_text(
                "Sorry, restarting the bot is restricted to its owners."
            )

    def filter_website(self, update, context):  # pylint: disable=unused-argument
        """
        This function tells the database to filter a specific website link or not.
        """
        chat_id = update.effective_chat.id
        message = update.message.text.split(" ")
        filtered_website = message[1].lower()  # Website name

        # Check if the website is supported.
        if filtered_website not in ["twitter", "tiktok", "instagram"]:
            update.message.reply_text("This website is not supported.")
        else:
            if message[2].lower() == "on":
                value = 1
            elif message[2].lower() == "off":
                value = 0
            else:
                update.message.reply_text("Please use 'on' or 'off'.")
                return
            # Set first letter of website to uppercase
            filtered_website_name = filtered_website[0].upper() + filtered_website[1:]
            update.message.reply_text(
                filtered_website_name + " embeds are: " + message[2]
            )
            self.db.edit_db(chat_id, filtered_website, value)
            # Update the local dictionary from the database.
            self.filter_db = self.db.get_db( # pylint: disable=attribute-defined-outside-init
                chat_id
            )
