"""Test the embeds bot."""
from unittest.mock import MagicMock, Mock
import fakeredis

from embeds_bot.gimme_embeds import GimmeEmbeds

mocked_update = MagicMock()
mocked_update.effective_chat.id = 0
mocked_update.message.text = "test message"
mocked_update.message.entities[0].url = "twitter.com"

mocked_context = Mock()
# mock a redis client
mock_redis = fakeredis.FakeStrictRedis(version=6)
mock_redis.get_db = MagicMock(return_value={
    "twitter": 1,
    "instagram": 0,
    "tiktok": 1
})
mock_redis.create_db = MagicMock()
mock_redis.edit_db = MagicMock()
ge = GimmeEmbeds(db=mock_redis)


def test_start():
    """Test the start function."""
    ge.start(mocked_update, mocked_context)
    mocked_context.bot.send_message.assert_called()


def test_source():
    """Test the source function."""
    ge.source(mocked_update, mocked_context)
    mocked_context.bot.send_message.assert_called()


def test_edit_text_twitter():
    """Test the edit_text function for Twitter."""
    assert (
        ge.edit_text(
            "twitter.com/prince/status/1380000000000000000",
            mocked_update.effective_chat.id,
        )
        == "vxtwitter.com/prince/status/1380000000000000000"
    )  # pylint: disable=line-too-long
    assert (
        ge.edit_text(
            "twitter.com/i/spaces/1380000000000000000", mocked_update.effective_chat.id
        )
        is None
    )
    assert (
        ge.edit_text(
            "twitter.com/i/events/1380000000000000000", mocked_update.effective_chat.id
        )
        is None
    )
    assert (
        ge.edit_text(
            "vxtwitter.com/prince/status/1380000000000000000",
            mocked_update.effective_chat.id,
        )
        is None
    )


def test_edit_text_tiktok():
    """Test the edit_text function for TikTok."""
    assert (
        ge.edit_text(
            "tiktok.com/@prince/video/6900000000000000000",
            mocked_update.effective_chat.id,
        )
        == "vxtiktok.com/@prince/video/6900000000000000000"
    )
    assert (
        ge.edit_text(
            "vxtiktok.com/@prince/video/6900000000000000000",
            mocked_update.effective_chat.id,
        )
        is None
    )


def test_edit_text_instagram():
    """Test the edit_text function for Instagram."""
    assert (
        ge.edit_text(
            "instagram.com/p/CO0000000000000000000/", mocked_update.effective_chat.id
        )
        == "ddinstagram.com/p/CO0000000000000000000/"
    )
    assert (
        ge.edit_text(
            "ddinstagram.com/p/CO0000000000000000000/", mocked_update.effective_chat.id
        )
        is None
    )


def test_edit_text_invalid():
    """Test the edit_text function for invalid URLs."""
    assert ge.edit_text("invalid_url", mocked_update.effective_chat.id) is None


def test_edit_text_empty():
    """Test the edit_text function for empty string."""
    assert ge.edit_text("", mocked_update.effective_chat.id) is None


def test_edit_text_no_url():
    """Test the edit_text function for no URL."""
    assert ge.edit_text("test message", mocked_update.effective_chat.id) is None
