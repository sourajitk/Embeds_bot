"""
Embeds here we come!
"""
import re
import sys


class GimmeEmbeds:
    def start(self, update, context):
        """
        This function sets up the /start action to let the user know the
        bot is alive and ready to go.
        """
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hello")

    def edit_text(self, text):
        """
        This function edits the text of the message, by replacing some
        website URLs with their vx counterparts that support embeds.
        """

        # Setup conditionals.
        # For Twitter
        if re.search(
            "(?P<url>twitter.com[^\s]+)", text, re.IGNORECASE
        ) and not re.search("(?P<url>xtwitter.com[^\s]+)", text, re.IGNORECASE):
            # Isolate the Twitter URL.
            twitter_url = str(
                re.search("(?P<url>twitter.com[^\s]+)", text, re.IGNORECASE).group(
                    "url"
                )
            )
            insensitive_twitter = re.compile(re.escape("twitter.com"), re.IGNORECASE)
            new_url = insensitive_twitter.sub("vxtwitter.com", twitter_url)
            new_url = new_url.split("?")[0]  # Remove trackers

        # For TikTok
        elif re.search(
            "(?P<url>tiktok.com[^\s]+)", text, re.IGNORECASE
        ) and not re.search("(?P<url>xtiktok.com[^\s]+)", text, re.IGNORECASE):
            # Isolate the tiktok URL.
            tiktok_url = str(
                re.search("(?P<url>tiktok[^\s]+)", text, re.IGNORECASE).group("url")
            )
            insensitive_tiktok = re.compile(re.escape("tiktok.com"), re.IGNORECASE)
            new_url = insensitive_tiktok.sub("vxtiktok.com", tiktok_url)
        return new_url

    def text_handler(self, update, context):
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
            reply(self.edit_text(message))
        else:
            url = update.message.entities[0].url
            reply(self.edit_text(url))

    def stop_and_restart():
        """
        Gracefully stop the Updater and replace the current 
        process with a new one
        """
        updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)
    
    def restart(update, context):
        update.message.reply_text("Bot is restarting...")
        Thread(target=stop_and_restart).start()