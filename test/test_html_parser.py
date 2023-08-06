import unittest

from temp.text_analysis.src.html_parser import TextAnalysis
import re


class TestTextAnalysis(unittest.TestCase):
    def setUp(self) -> None:
        url = "https://www.volvogroup.com/en/careers/diversity-and-inclusion/accelerating-gender-diversity.html"
        self.obj = TextAnalysis(url)
        self.data = self.obj.parse_html_without_re()
        self.data_re = self.obj.parse_html_with_re()
        self.expected_count = [('the', 78), ('to', 75), ('and', 61), ('of', 55), ('Volvo', 47), ('a', 42), ('in', 39),
                               ('Group', 33), ('is', 28), ('for', 26)]

    def test_parse_html_with_re(self):
        self.assertFalse(re.search(r'<.[^>]*>', self.data_re))
        self.assertFalse(re.search(r'<style|<script', self.data_re))
        self.assertFalse(re.search(r'[^\w\s]', self.data_re))

    def test_parse_html_without_re(self):
        self.assertFalse(re.search(r'<.[^>]*>', self.data))
        self.assertFalse(re.search(r'<style|<script', self.data))
        self.assertFalse(re.search(r'[^\w\s]', self.data))

    def test_count_word(self):
        count = self.obj.count_word(self.data)
        self.assertEqual(count, self.expected_count)

        count = self.obj.count_word(self.data_re)
        self.assertEqual(count, self.expected_count)


if __name__ == '__main__':
    unittest.main()
