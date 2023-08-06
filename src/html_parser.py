import requests
from collections import Counter
import re


class TextAnalysis:
    def __init__(self, html_url):
        self.url = html_url

    def parse_html_with_re(self):

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

        final_string = re.sub(r'[^\w\s]', '', text)  # removing punctuation and special chars

        return final_string

    def parse_html_without_re(self):
        res = requests.get(url=self.url)
        html_content = res.text
        words_list = []
        html_content = html_content.replace('<', ' <').replace('>', '> ').split('>')
        i = 0

        while i < len(html_content):
            if html_content[i].strip().startswith('<head '):
                while not html_content[i].strip().startswith('</head') and i < len(html_content):
                    i += 1
                    continue

            elif html_content[i].strip().startswith('<style'):
                while i < len(html_content) and not html_content[i].strip().startswith('</style'):
                    i += 1
                    continue

            elif html_content[i].strip().startswith('<script'):
                while i < len(html_content) and not html_content[i].strip().startswith('</script'):
                    i += 1
                    continue

            elif html_content[i].strip().startswith('<footer'):
                while not html_content[i].strip().startswith('</footer') and i < len(html_content):
                    i += 1
                    continue

            elif not (html_content[i].strip().startswith('<') or (html_content[i].strip().endswith(';')
                      and html_content[i].strip().startswith('&')) or html_content[i].strip().startswith('href=')
                      or html_content[i].strip().startswith('rel=') or html_content[i].strip().startswith('target=')):
                for line in html_content[i].split():
                    if not (line.strip().startswith('<') or (line.strip().endswith(';') and line.strip().startswith('&'))
                            or line.strip().startswith('href=') or line.strip().startswith('rel=')
                            or line.strip().startswith('target=')):
                        new_line = ''.join(l for l in line if (l.isalnum() or l.isspace()))
                        words_list.append(new_line)
            i += 1
        return " ".join(words_list)

    def count_word(self, data):
        # Count word occurrence and write in file
        data = data.split()
        count_list = Counter(data)
        result = count_list.most_common(10)

        return result

    def write_result(self, result, data=None):
        if data:
            with open('../parsed_data.txt', 'w') as f:  # Parsed html in file
                f.write(' '.join(data.split()))
        with open('../result.txt', 'w') as r:
            r.writelines([f"{res}\n" for res in result])  # Occurrences in file


if __name__ == "__main__":
    url = "https://www.volvogroup.com/en/careers/diversity-and-inclusion/accelerating-gender-diversity.html"
    #url = "https://www.volvogroup.com/en/news-and-media/portraits/portraits/meet-juliane-tosin.html"
    obj = TextAnalysis(url)
    parsed_data = obj.parse_html_without_re()
    #parsed_data = obj.parse_html_with_re()
    count = obj.count_word(parsed_data)
    obj.write_result(count)


