__author__ = 'sakuratanoshiminaki'
import os.path
import dicts
import random

def load_words(*files):
        words = WordList()
        for file in files:
            with open(os.path.abspath(file)) as f:
                for line in f.readlines():
                    line = line.rstrip("\n")
                    words.append(Word(line))
        return words

class Word:
    word = ""
    definition = ""

    def __init__(self, word, definition=""):
        self.word = word
        self.definition = definition
    def get_word(self):
        return self.word
    def get_definition(self):
        if self.definition == "":
            self.definition = "".join(dicts.get_definition(self.word))
        return self.definition

class WordList(list):
    def __init__(self, *words, index=False, definition=False):
        self.extend(words)
        self.__idx=index
        self.__def=definition
    def set_idx(self, index):
        self.__idx = index
    def set_def(self, definition):
        self.__def = definition
    def shuffle(self):
        random.shuffle(self)
    def solve_redundancy(self):
        word_dict = set()
        for idx, word in enumerate(self):
            if word.get_word() in word_dict:
                self.pop(idx)
            word_dict.add(word.get_word())

    def __str__(self):
        self.__repr__()
    def __repr__(self):
        result = ""
        for idx, word in enumerate(self, start=1):
            idx_str = str(idx) + ": " if self.__idx else ""
            definition_str = ": " + word.get_definition() if self.__def else ""
            result = result + idx_str + word.get_word() + definition_str + "\n"
        return result