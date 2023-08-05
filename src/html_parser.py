import requests
from collections import Counter
import re


class TextAnalysis:
    def __init__(self, html_url):
        self.url = html_url

    def parse_html(self):

        res = requests.get(url=self.url)

        pattern = r'<footer class=.*?>(.*?)footer>'  # removing footer
        text = re.sub(pattern, '', res.text, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

        pattern = r'<head class=.*?>(.*?)head>'  # removing header
        text = re.sub(pattern, '', text, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

        pattern = r'<style.*?\/[ ]*style>'  # removing css
        text = re.sub(pattern, '', text, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

        pattern = r'<script.*?>(.*?)script>'  # removing js
        text = re.sub(pattern, '', text, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))

        pattern = re.compile('<.[^>]*>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        text = re.sub(pattern, '', text)  # removing div

        new_string = re.sub(r'[^\w\s]', ' ', text)  # removing punctuation and special chars

        return new_string

    def count_word(self, data):
        # Count word occurrence and write in file
        words_list = data.split()

        count_list = Counter(words_list)
        result = count_list.most_common(10)

        return result

    def write_result(self, result):

        # with open('../parsed_data.txt', 'w') as f:  # Parsed html in file
        #     f.write(' '.join(words_list.split()))
        with open('../result.txt', 'w') as r:
            r.writelines([f"{res}\n" for res in result])  # Occurrences in file


if __name__ == "__main__":
    url = "https://www.volvogroup.com/en/careers/diversity-and-inclusion/accelerating-gender-diversity.html"
    #url = "https://www.volvogroup.com/en/news-and-media/portraits/portraits/meet-juliane-tosin.html"
    obj = TextAnalysis(url)
    parsed_data = obj.parse_html()
    count = obj.count_word(parsed_data)
    obj.write_result(count)


