from webside import extract_title
import unittest
class testExtractTitle(unittest.TestCase):
    def test_h1(self):
        title = extract_title("# hello")
        self.assertEqual(title,"hello")

    def test_h1_whitespace(self):
        title = extract_title("#     hello      ")
        self.assertEqual(title,"hello")