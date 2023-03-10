import unittest

from BiliStreamer.biliStream import Streamer

class TestCalculator(unittest.TestCase):
    def test_add(self):
        calc = Streamer()
        self.assertEqual(calc.add(2, 3), 5)

if __name__ == '__main__':
    unittest.main()