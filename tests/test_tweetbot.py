import os
from unittest import mock

import tweetbot


class MockApi:
    def status_post(self, text):
        assert (
            text
            == "예문 1 https://femiwiki.com/w/%EB%AC%B8%EC%84%9C%201%20"
            + "?utm_campaign=bot&utm_source=fediverse&utm_medium=post"
        )
        return {"id": 0}


class MockPage:
    def text(self):
        return ""

    def save(self, text, title):
        pass


class MockSite:
    def __init__(self):
        self.pages = {tweetbot.RECENT_POSTS_PAGE_NAME: MockPage()}

    def api(self, action, page="", prop="", formatversion=2):
        return {
            "parse": {
                "wikitext": """
== 문서 1 ==

* 예문 1
"""
            }
        }


@mock.patch.dict(os.environ, {"MASTODON_ACCESS_TOKEN": ""})
@mock.patch.dict(os.environ, {"FEMIWIKI_OAUTH1_CONSUMER_TOKEN": ""})
@mock.patch.dict(os.environ, {"FEMIWIKI_OAUTH1_CONSUMER_SECRET": ""})
@mock.patch.dict(os.environ, {"FEMIWIKI_OAUTH1_ACCESS_TOKEN": ""})
@mock.patch.dict(os.environ, {"FEMIWIKI_OAUTH1_ACCESS_SECRET": ""})
def test_main(mocker):
    mocker.patch("mwclient.page.Page.save", return_value=None)
    mocker.patch(
        "mwclient.listing.PageList", return_value={tweetbot.RECENT_POSTS_PAGE_NAME: ""}
    )
    mocker.patch("mwclient.Site", return_value=MockSite())
    mocker.patch("mastodon.Mastodon", return_value=MockApi())

    tweetbot.main()


def test_short_text():
    expected = ["1234567890"]
    actual = list(tweetbot.break_text("1234567890", 10))
    assert expected == actual


def test_two_lines():
    expected = ["123 4567…", "…890 ab"]
    actual = list(tweetbot.break_text("123 4567 890 ab", 10))
    assert expected == actual

    expected = ["123 4567…", "…890 abc"]
    actual = list(tweetbot.break_text("123 4567 890 abc", 10))
    assert expected == actual


def test_three_lines():
    expected = ["123 4567…", "…890 abcd…", "…efg"]
    actual = list(tweetbot.break_text("123 4567 890 abcd efg", 10))
    assert expected == actual
