"""Setup a database to permanenly store the bot's settings for each user."""
import os
import redis


class GimmeDB:
    """Class to handle the bot's database."""

    def create_db(self, chat_id):
        """Create a database for the chat."""
        redis_db = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379, db=0)

        # Check if a group is already in the database and if not, create it using hashes
        if not redis_db.sismember("groups", chat_id):
            redis_db.sadd("groups", chat_id)
            redis_db.hset(f"group_{format(chat_id)}", "twitter", 1)
            redis_db.hset(f"group_{format(chat_id)}", "instagram", 1)
            redis_db.hset(f"group_{format(chat_id)}", "tiktok", 1)
        return redis_db.hgetall(f"group_{format(chat_id)}")

    def edit_db(self, chat_id, website, value):
        """Edit the database for the chat."""
        redis_db = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379, db=0)
        updated = redis_db.hset(f"group_{format(chat_id)}", website, value)
        return updated

    def get_db(self, chat_id):
        """Get the database for the chat in a dictionary."""
        redis_db = redis.Redis(host=os.getenv("REDIS_HOST"), port=6379, db=0)
        # Create a dictionary from the database
        dictionay_db = {
            k.decode("utf-8"): v.decode("utf-8")
            for k, v in redis_db.hgetall(f"group_{format(chat_id)}").items()
        }
        return dictionay_db
