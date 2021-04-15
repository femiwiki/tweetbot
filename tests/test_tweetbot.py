import unittest

import tweetbot


class TestTweetbot(unittest.TestCase):

    def test_short_text(self):
        expected = ['1234567890']
        actual = list(tweetbot.break_text('1234567890', 10))
        assert expected == actual

    def test_two_lines(self):
        expected = ['123 4567…', '…890 ab']
        actual = list(tweetbot.break_text('123 4567 890 ab', 10))
        assert expected == actual

        expected = ['123 4567…', '…890 abc']
        actual = list(tweetbot.break_text('123 4567 890 abc', 10))
        assert expected == actual

    def test_three_lines(self):
        expected = ['123 4567…', '…890…', '…abcd…', '…efg']
        actual = list(tweetbot.break_text('123 4567 890 abcd efg', 10))
        assert expected == actual


if __name__ == '__main__':
    unittest.main()
