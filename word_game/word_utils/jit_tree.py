from .find_pangram import related_words

class JitTree:
    def __init__(self, root, words):
        self.words = [root] + list(set(words) - {root})
        self.parents = [-1] * len(self.words)
        self.levels = [-1] * len(self.words)
        self.levels[0] = 0
        self.assign_parents()

    def assign_parents(self):
        prior_level = [0]
        level_count = 1
        next_level = []
        while len(prior_level) > 0:
            for i in range(1, len(self.words)):
                if self.parents[i] != -1:
                    continue
                for j in prior_level:
                    if related_words(self.words[i], self.words[j]):
                        next_level.append(i)
                        self.parents[i] = j
                        self.levels[i] = level_count
            level_count += 1
            prior_level = next_level
            next_level = []

    def ordered_nodes(self):
        nodes = {}
        for i in range(len(self.words)):
            nodes[i] = self.JitNode(self.parents[i], self.levels[i], self.words[i])
        for k, v in nodes.items():
            if v.parent >= 0:
                nodes[v.parent].children.append(v)
        return nodes[0].append_children()

    class JitNode:
        def __init__(self, parent, level, word):
            self.parent = parent
            self.level = level
            self.word = word
            self.children = []

        def append_children(self):
            output = [self]
            for child in self.children:
                output += child.append_children()
            return output


