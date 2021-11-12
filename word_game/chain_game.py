from random import sample

from .word_utils.find_pangram import *
from .word_utils.jit_tree import JitTree
from .base_game import BaseGame

class ChainGame(BaseGame):
    def __init__(self, first_word):
        if first_word is None:
            first_word = sample(pangram_candidates(), 1)[0]
        first_word = first_word.lower()
        self.first_word_set = self.word_hash(first_word)
        self.words = {f"{self.first_word_set}": {first_word}}
        self.first_word = first_word

    def word_hash(self, word):
        return ''.join(sorted(list(set(word))))

    def add_word(self, word):
        s = self.word_hash(word)
        if s in self.words:
            self.words[s].add(word)
        else:
            self.words[s] = {word}

    def points(self):
        p = 0
        for h, w in self.words.items():
            p += len(w) ** 2
        return p

    def word_display(self):
        output = ""
        tree = JitTree(self.first_word_set, self.words.keys()).ordered_nodes()
        for node in tree:
            output += '\n '
            old = set_difference(node.word.upper(), self.first_word.upper())
            new = set_difference(self.first_word.upper(), node.word.upper())
            shared = intersect(node.word.upper(), self.first_word.upper())
            output += old + " " * (1 + node.level - len(old)) + " "
            output += shared + "  " + new + "  |  "
            output += " ".join(self.words[node.word])
        return output

    def input_string(self):
        words = f"words:{self.word_display()}"
        return chr(27) + f"[2J\n{words}\n\n"

    def guess(self, word):
        word = word.lower()
        if word in pangram_candidates():
            for i in self.words:
                if related_words(i, word):
                    self.add_word(word)
                    self.save_game()
                    break

    def found_words(self):
        words = []
        for k, v in self.words.items():
            for word in v:
                words.append(word)
        return words


def game():
    return ChainGame

def start(first_word=None):
    h = ChainGame(first_word)
    h.wait_for_input()

def load_game(word):
    h = None
    with open(f"saved_games/{word}.chngm", "r") as f:
        h = ChainGame(word)
        lines = f.read().splitlines()
        for l in lines:
            h.add_word(l)
    h.wait_for_input()
