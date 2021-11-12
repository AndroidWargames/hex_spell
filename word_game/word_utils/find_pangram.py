import functools
from pathlib import Path

COMMON_WORDS_PATH = Path(__file__).parent / "./reference/common_words.txt"

def memoize(func):
    cache = func.cache = {}
    @functools.wraps(func)
    def memoized_func(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return memoized_func


@memoize
def all_words():
    with open(COMMON_WORDS_PATH, "r") as f:
        return f.read().splitlines()


@memoize
def pangram_candidates():
    words = filter(pangram_length, all_words())
    words = filter(can_pangram, words)
    return list(words)


def pangram_length(word):
    l = len(word)
    return 7 <= l and l <= 12


def length_filter(length):
    return lambda x: len(x) == length


def subset_length(word):
    return len(word) >= 4


def can_pangram(word):
    return len(set(word)) == 7


def get_words(word):
    return filter_subsets(all_words(), word)


def filter_letter(words, letter):
    return list(filter(lambda x: letter in x, words))


def filter_subsets(words, pangram):
    return list(filter(lambda x: set(x).issubset(pangram), words))


def multiple_pangrams(word):
    return number_of_pangrams(word) > 1

def number_of_pangrams(word):
    return len(filter_subsets(pangram_candidates(), word))

def related_words(a, b):
    return related_sets(set(a), set(b))

def reduceable_to(a, b):
    return len(set(a)) - len(set(b)) == 1 and related_words(a, b)

def related_sets(a, b):
    return set_distance(a, b) <= 1

def distant_sets(a, b):
    return set_distance(a, b) > min(list(map(len, [a, b])))

def set_distance(a, b):
    return max(len(a - b), len(b - a))

def set_difference(a, b):
    return ''.join(set(b) - set(a))

def intersect(a, b):
    return ''.join(set(a).intersection(b))
