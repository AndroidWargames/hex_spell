from find_pangram import *
from random import sample
from jit_tree import JitTree
from word_game.base_game import BaseGame

class ReductionGame(BaseGame):
    def __init__(self, first_word):
        if first_word is None:
            candidates = list(filter(length_filter(4), all_words()))
            candidates = list(filter(lambda x: len(set(x)) == 3, candidates))
            first_word = sample(candidates, 1)[0]
        first_word = first_word.lower()
        self.first_word_set = self.word_hash(first_word)
        self.words = dict()
        self.guessable_words = set()
        self.first_word = first_word
        self.add_word(self.first_word)

    def word_hash(self, word):
        return ''.join(sorted(list(set(word))))

    def add_word(self, word):
        s = self.word_hash(word)
        if s in self.words:
            self.words[s].add(word)
        else:
            self.words[s] = {word}
        self.add_new_guessable(word)

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
            old = set_difference(self.first_word.upper(), node.word.upper())
            shared = intersect(node.word.upper(), self.first_word.upper())
            output += shared + " " + old + " "
            output += " ".join(self.words[node.word])
        return output

    def input_string(self):
        words = f"words:{self.word_display()}"
        return chr(27) + f"[2J\n{words}\n\n"

    def wait_for_input(self):
        i = input(self.input_string())
        if i == 'h':
            self.help()
        elif i == "H":
            print(self.first_word_set)
        elif i == "x":
            return
        else:
            self.guess(i)
        self.wait_for_input()

    def guess(self, word):
        word = word.lower()
        if word in self.guessable_words:
            self.add_word(word)
            self.save_game()

    def add_new_guessable(self, new_word):
        for word in all_words():
            if reduceable_to(word, new_word):
                self.guessable_words.add(word)

    def found_words(self):
        words = []
        for k, v in self.words.items():
            for word in v:
                words.append(word)
        return words

def start(first_word=None):
    h = ReductionGame(first_word)
    h.wait_for_input()

def load(word):
    h = None
    with open(f"saved_games/{word}.redgm", "r") as f:
        h = ReductionGame(word)
        lines = f.read().splitlines()
        for l in lines:
            h.add_word(l)
    h.wait_for_input()
