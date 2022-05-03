import json
import re
from io import TextIOWrapper
from collections import defaultdict

class frequency:

    def __init__(self, file_name: str):
        self._freq = defaultdict(lambda: 0, {})
        regex1 = re.compile('[^a-zA-Z ]')
        regex2 = re.compile('[—\-\n+]')
        with open(file_name, encoding='utf8') as file:
            file_text = regex1.sub('', regex2.sub(' ', file.read()))
        words = file_text.split()
        for w in words:
            self._freq[w.lower()] += 1
        self.words = list(self._freq.keys())
        self.freq = list(self._freq.values())

if __name__ == "__main__":
    freq = frequency("example generator/Thing_Explainer.txt")
    with open('example generator/common_words.txt', 'w') as convert_file:
        convert_file.write(json.dumps(freq._freq))
