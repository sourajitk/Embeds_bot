"""Setup a database to permanenly store the bot's settings for each user."""
import redis


class GimmeDB:
    """Class to handle the bot's database."""

    def __init__(self, redis_host: str = None, redis_port: int = None, password: str = None):
        self.redis_host = redis_host or "localhost"
        self.redis_port = redis_port or 6379
        self.redis_password = password or None
        self.redis_db = redis.Redis(host=self.redis_host, port=self.redis_port, db=0, password=self.redis_password) # pylint: disable=line-too-long

    def create_db(self, chat_id):
        """Create a database for the chat."""
        # Check if a group is already in the database and if not, create it using hashes
        if not self.redis_db.sismember("groups", chat_id):
            self.redis_db.sadd("groups", chat_id)
            self.redis_db.hset(f"group_{format(chat_id)}", "twitter", 1)
            self.redis_db.hset(f"group_{format(chat_id)}", "instagram", 1)
            self.redis_db.hset(f"group_{format(chat_id)}", "tiktok", 1)
        return self.redis_db.hgetall(f"group_{format(chat_id)}")

    def edit_db(self, chat_id, website, value):
        """Edit the database for the chat."""
        updated = self.redis_db.hset(f"group_{format(chat_id)}", website, value)
        return updated

    def get_db(self, chat_id):
        """Get the database for the chat in a dictionary."""
        # Create a dictionary from the database
        dictionay_db = {
            k.decode("utf-8"): v.decode("utf-8")
            for k, v in self.redis_db.hgetall(f"group_{format(chat_id)}").items()
        }
        return dictionay_db
