import random
import re
import nltk
from nltk import bigrams, trigrams, ConditionalFreqDist


class TextGenerator:

    def __init__(self):
        self.statistics = {"all": 0, "unique": 0}
        self.file = []
        self.all = []
        self.bigrams = []
        self.trigrams = []
        self.b_markov = {}
        self.t_markov = {}

    def get_file(self):
        directory = input()  # uncomment this to use your own corpus
        # directory = "_corpus.txt"  # comment this to use your own corpus
        with open(directory, "r", encoding="utf-8") as f:
            self.file = f.read()

    def get_statistics(self):
        self.all = self.file.split()
        freq = nltk.FreqDist(self.all)
        self.statistics["all"] = len(self.all)
        self.statistics["unique"] = len(freq)
        # self.get_bigrams()
        self.get_trigrams()

    def get_bigrams(self):
        # My own method to get bigrams
        # for i in range(1, len(self.all)):
        #     self.bigrams.append([self.all[i - 1], self.all[i]])
        self.bigrams = bigrams(self.all)
        self.get_markov(_bigrams=True)

    def get_trigrams(self):
        self.trigrams = trigrams(self.all)
        self.get_markov(_trigrams=True)

    def get_markov(self, _bigrams=False, _trigrams=False):
        # My own method to create a Markov chain Model
        # markov_dict = defaultdict(list)
        # for bigram in self.bigrams:
        #     markov_dict[bigram[0]].append(bigram[1])
        # for k, v in markov_dict.items():
        #     self.markov[k] = Counter(v)
        if _bigrams:
            self.b_markov = ConditionalFreqDist(self.bigrams)
        elif _trigrams:
            condition = (((x, y), z) for x, y, z in self.trigrams)
            self.t_markov = ConditionalFreqDist(condition)

    def get_unique_word(self, text=None, start=False):
        if start:
            while True:
                word = random.choice(list(self.t_markov.keys()))
                has_suitable = self.test_next_word(word)
                if re.match("[A-Z][^.!?]+$", word[0]) and re.match("[^.!?]+$", word[1]) and has_suitable:
                    return word
        else:
            population = []
            weights = []
            head = (text[-2], text[-1])
            for k, v in self.t_markov[head].most_common():
                population.append(k)
                weights.append(v)
            while True:
                word = random.choices(population=population, weights=weights)[0]
                index = population.index(word)
                del population[index]
                del weights[index]
                if len(text) < 4:
                    has_suitable = self.test_next_word(text, word)
                    if re.match("[^.!?]+$", word) and has_suitable:
                        return word
                else:
                    return word

    def test_next_word(self, text, word=""):
        new = list(text)
        if word != "":
            new.append(word)
        head = (text[-2], text[-1])
        has_suitable = False
        for k, v in self.t_markov[head].most_common():
            if len(new) < 5:
                if re.match("[^.!?]+$", k):
                    has_suitable = self.test_next_word(new, k)
            else:
                has_suitable = True
        return has_suitable

    def generate_strings(self, count):
        for x in range(count):
            word1, word2 = self.get_unique_word(start=True)
            text = [word1, word2]
            while True:
                word = self.get_unique_word(text)
                if re.match(".+[.?!]", word):
                    text.append(word)
                    break
                text.append(word)
            text = " ".join(text)
            print(text)

    def main(self):
        self.get_file()
        self.get_statistics()
        self.generate_strings(10)


# nltk.download("punkt")  # Download if getting punkt error
if __name__ == "__main__":
    TextGenerator().main()
