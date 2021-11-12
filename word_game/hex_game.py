from find_pangram import pangram_candidates, get_words, filter_letter, can_pangram
from random import sample
from word_game.base_game import BaseGame


class HexGame(BaseGame):
    def __init__(self):
        self.first_word = sample(pangram_candidates(), 1)[0]
        self.main_letter = sample(set(self.first_word), 1)[0]
        self.secret_words = filter_letter(
                get_words(self.first_word),
                self.main_letter
            )
        self.guessed_words = []

    def print_guessed_words(self):
        print('\t'.join(guessed_words))

    def points(self, words):
        p = 0
        for w in words:
            l = len(w)
            if l == 4:
                p += 1
            else:
                p += l
            if can_pangram(w):
                p += 7
        return p


    def input_string(self):
        points = f"points: {self.points(self.guessed_words)}/{self.points(self.secret_words)}"
        words = f"words: {len(self.guessed_words)}/{len(self.secret_words)}"
        s = set(self.first_word)
        s.remove(self.main_letter)
        letters = f"{self.main_letter} | {' '.join(s)}"
        return f"\n{letters}\n{points}\t\t{words}\n"

    def guess(self, word):
        word = word.lower()
        if word in self.guessed_words:
            print(f"Already Guessed {word}")
        elif word in self.secret_words:
            print(f"{word}: {self.points([word])} points!")
            self.guessed_words.append(word)
        elif self.main_letter not in word:
            print("missing main letter")
        else:
            print("Nope!")

    def found_words(self):
        return self.guessed_words


def start(seed=None):
    h = HexGame()
    h.wait_for_input()
