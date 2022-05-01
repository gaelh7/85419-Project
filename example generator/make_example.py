
import random
import re
from word_forms.word_forms import get_word_forms
from itertools import chain
from string import ascii_lowercase as alph

alph += " "
alph = {k: v for v, k in enumerate(alph)}

def transform_word(word : str):
    forms = tuple(set(chain(*get_word_forms(word, 0.9).values())))
    new_word = word if len(forms) == 0 else random.choice(forms)
    return re.sub('[^a-zA-Z]', '', new_word)

class example:

    @staticmethod
    def example_string(sent : str, dataset : str) -> str:
        """
        Take in a string (sentence) and produce a lens
        example
        """
        example = f"{len(sent) - sent.count(' ')}\n"
        sent = sent.lower()
        sent += " "
        skip = False
        i = 0
        for c, s in enumerate(sent[:-1]):
            if skip:
                skip = False
                continue
            next = sent[c + 1]
            if next == ' ' and c + 2 < len(sent):
                next2 = sent[c + 2]
                if dataset == "train":
                    example += f"[{i}] i:{alph[s]} t:{alph[next2]} {alph[next]}\n"
                elif dataset == "test":
                    example += f"[{i}] i:{alph[s]} t:{alph[next]}\n"
                skip = True
            else:
                if dataset == "train" or c + 2 == len(sent):
                    example += f"[{i}] i:{alph[s]} t:{alph[next]}\n"
                elif dataset == "test":
                    example += f"[{i}] i:{alph[s]}\n"
            i += 1
        example += ";"
        return example

    def generate_sentence(self, min_len : int, max_len : int):
        pass

    def generate_example(self, min_len : int, max_len : int, dataset : str):
        sent = self.generate_sentence(min_len, max_len)
        return self.example_string(sent, dataset)

class random_example(example):

    def __init__(self, file : str) -> None:
        word_file = open(file)
        word_list = word_file.read().splitlines()
        word_file.close()
        self.words = word_list

    def generate_sentence(self, min_len : int, max_len : int):
        sent = random.choice(self.words)
        word = transform_word(random.choice(self.words))
        while len(sent) + len(word) - sent.count(' ') <= max_len:
            sent += f" {word}"
            word = transform_word(random.choice(self.words))
        if len(sent) - sent.count(' ') < min_len:
            return self.generate_sentence(min_len, max_len)
        return sent



class text_example(example):

    def __init__(self, file : str):
        text_file = open(file, encoding='utf8')
        par_list = text_file.read().split("\n\n")
        text_file.close()
        regex1 = re.compile('[^a-zA-Z ]')
        regex2 = re.compile('[—\-\n]')
        par_list = map(lambda s : regex1.sub('', regex2.sub(' ', s)), par_list)
        self.lines = list(par_list)

    def generate_sentence(self, min_len : int, max_len : int):
        curr = random.choice(self.lines).split()
        idx = random.choice(range(len(curr)))
        sent = ''
        while idx < len(curr):
            word = curr[idx]
            if len(sent) + len(word) - sent.count(' ') > max_len:
                break
            sent += f'{word} '
            idx += 1
        if len(sent) - sent.count(' ') < min_len:
            return self.generate_sentence(min_len, max_len)
        return sent[:-1]
