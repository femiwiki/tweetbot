from tweetbot import break_text


def test_short_text():
    expected = ['1234567890']
    actual = list(break_text('1234567890', 10))
    assert expected == actual


def test_two_lines():
    expected = ['123 4567…', '…890 ab']
    actual = list(break_text('123 4567 890 ab', 10))
    assert expected == actual

    expected = ['123 4567…', '…890 abc']
    actual = list(break_text('123 4567 890 abc', 10))
    assert expected == actual


def test_three_lines():
    expected = ['123 4567…', '…890…', '…abcd…', '…efg']
    actual = list(break_text('123 4567 890 abcd efg', 10))
    assert expected == actual
