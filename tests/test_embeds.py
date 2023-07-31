"""Test the embeds bot."""
from unittest.mock import MagicMock, Mock
import fakeredis
import pytest
from embeds_bot.gimme_embeds import GimmeEmbeds

mocked_update = MagicMock()
mocked_update.effective_chat.id = 0
mocked_update.message.text = "test message"
mocked_update.message.entities[0].url = "twitter.com"

mocked_context = Mock()
# mock a redis client
mock_redis = fakeredis.FakeStrictRedis(version=6)
mock_redis.get_db = MagicMock(return_value={"twitter": 1, "instagram": 1, "tiktok": 1})
mock_redis.create_db = MagicMock()
mock_redis.edit_db = MagicMock()
ge = GimmeEmbeds(db=mock_redis)


def assert_edit_text_unchanged(url):  # pylint: disable=missing-function-docstring
    assert ge.edit_text(url, mocked_update.effective_chat.id) is None


@pytest.mark.parametrize(
    "url,expected",
    [
        ("twitter.com/...", "vxtwitter.com/..."),
        ("tiktok.com/...", "vxtiktok.com/..."),
        ("instagram.com/...", "ddinstagram.com/..."),
    ],
)
def test_edit_text(url, expected):  # pylint: disable=missing-function-docstring
    assert ge.edit_text(url, mocked_update.effective_chat.id) == expected
    mock_redis.edit_db.assert_called_with(
        mocked_update.effective_chat.id, ..., expected
    )
    assert_edit_text_unchanged(expected)


def test_start():  # pylint: disable=missing-function-docstring
    ge.start(mocked_update, mocked_context)
    mocked_context.bot.send_message.assert_called()
    mock_redis.create_db.assert_called_with(mocked_update.effective_chat.id)


def test_source():  # pylint: disable=missing-function-docstring
    ge.source(mocked_update, mocked_context)
    mocked_context.bot.send_message.assert_called()
