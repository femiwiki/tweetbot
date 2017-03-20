import unittest

from tweet import break_text


class TextBreakingTestCase(unittest.TestCase):
    def test_short_text(self):
        expected = ['1234567890']
        actual = list(break_text('1234567890', 10))
        self.assertListEqual(expected, actual)

    def test_two_lines(self):
        expected = ['123 4567 ..', '.. 890 ab']
        actual = list(break_text('123 4567 890 ab', 10))
        self.assertListEqual(expected, actual)

        expected = ['123 4567 ..', '.. 890 ..', '.. abc']
        actual = list(break_text('123 4567 890 abc', 10))
        self.assertListEqual(expected, actual)

    def test_three_lines(self):
        expected = ['123 4567 ..', '.. 890 ..', '.. abcd ..', '.. efg']
        actual = list(break_text('123 4567 890 abcd efg', 10))
        self.assertListEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
