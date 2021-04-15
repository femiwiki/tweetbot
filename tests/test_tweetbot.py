import tweetbot

import os
from unittest import mock

class MockApi:
    def PostUpdate(self, text):
        assert text == "예문 1 https://femiwiki.com/w/%EB%AC%B8%EC%84%9C%201%20?utm_campaign=bot&utm_source=twitter&utm_medium=tweet"
        return {"id":0}

class MockResponse:
    def read(self):
        return """
== 문서 1 ==

* 예문 1
""".encode('utf-8')

    def __enter__(self):
        return self

    def __exit__(self, a, b, c):
        pass


@mock.patch.dict(os.environ, {"TWITTER_CONSUMER_KEY": ""})
@mock.patch.dict(os.environ, {"TWITTER_CONSUMER_SECRET": ""})
@mock.patch.dict(os.environ, {"TWITTER_ACCESS_TOKEN": ""})
@mock.patch.dict(os.environ, {"TWITTER_ACCESS_TOKEN_SECRET": ""})
def test_main(mocker):
    mocker.patch(
        'mwclient.page.Page.save',
        return_value=None #
    )
    mocker.patch(
        'mwclient.listing.PageList',
        return_value={tweetbot.RECENT_TWEETS_PAGE_NAME: ""}
    )
    mocker.patch(
        'mwclient.Site.login',
        return_value=None
    )
    mocker.patch(
        'mwclient.Site',
        return_value=None
    )
    mocker.patch(
        'twitter.Api',
        return_value=MockApi()
    )
    mocker.patch(
        'urllib.request.urlopen',
        return_value=MockResponse()
    )

    tweetbot.main()


def test_short_text():
    expected = ['1234567890']
    actual = list(tweetbot.break_text('1234567890', 10))
    assert expected == actual


def test_two_lines():
    expected = ['123 4567…', '…890 ab']
    actual = list(tweetbot.break_text('123 4567 890 ab', 10))
    assert expected == actual

    expected = ['123 4567…', '…890 abc']
    actual = list(tweetbot.break_text('123 4567 890 abc', 10))
    assert expected == actual


def test_three_lines():
    expected = ['123 4567…', '…890…', '…abcd…', '…efg']
    actual = list(tweetbot.break_text('123 4567 890 abcd efg', 10))
    assert expected == actual
