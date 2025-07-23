import unittest
from gencontent import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_h1(self):
        md = """
# Hello

My name Jeff
"""
        title = extract_title(md)
        self.assertEqual("Hello", title)


    def test_missing_h1(self):
        md = """
## Hello

My name Jeff
"""
        with self.assertRaises(ValueError) as e:
            title = extract_title(md)
        msg = str(e.exception)
        self.assertEqual(msg, "title missing or invalid")
