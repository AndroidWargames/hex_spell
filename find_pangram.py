import functools


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
    with open("common_words.txt", "r") as f:
        return f.read().splitlines()


@memoize
def pangram_candidates():
    words = filter(pangram_length, all_words())
    words = filter(can_pangram, words)
    return list(words)


def pangram_length(word):
    l = len(word)
    return 7 <= l and l <= 10


def subset_length(word):
    return len(word) >= 4


def can_pangram(word):
    return len(set(word)) == 7 and 'er' not in word and 's' not in word and 'ed' not in word


def get_words(word):
    return filter_subsets(all_words(), word)


def filter_letter(words, letter):
    return list(filter(lambda x: letter in x, words))


def filter_subsets(words, pangram):
    return list(filter(lambda x: set(x).issubset(pangram), words))


def multiple_pangrams(word):
    other_grams = pangram_candidates()
    return len(filter_subsets(other_grams, word)) > 1
