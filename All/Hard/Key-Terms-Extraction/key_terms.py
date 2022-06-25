import string
from lxml import etree
import nltk
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


class KTE:

    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.file = 'news.xml'
        self.contents = {}  # Headers and their content

    def lemmatize_words(self, words):
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(word) for word in words]

    def clear_data(self, words):
        punctuations = string.punctuation
        sw_list = stopwords.words("english")
        return [word for word in words if word not in punctuations and word not in sw_list]

    def get_tagged(self, words, tag=""):
        tagged = [nltk.pos_tag([word]) for word in words]
        # print(tagged)
        result = [w for tag_tuple in tagged for w, w_tag in tag_tuple if w_tag == tag]
        return result

    def get_file(self):
        # self.file = input()
        self.get_members()

    def get_members(self):
        root = etree.parse(self.file).getroot()
        # root = etree.fromstring(self.file)
        for news in root[0]:
            self.contents[news[0].text] = news[1].text
        self.format_texts()

    def format_texts(self):
        for k, v in self.contents.items():
            words = word_tokenize(v.lower())
            words = self.lemmatize_words(words)
            words = self.get_tagged(self.clear_data(words), "NN")
            self.contents[k] = " ".join(words)
        tfidf_scores = self.vectorizer.fit_transform(self.contents.values()).toarray()
        tfidf_words = self.vectorizer.get_feature_names_out()
        self.print_freq_words(tfidf_scores, tfidf_words)

    def print_freq_words(self, scores, words):
        heads = list(self.contents.keys())
        for i in range(len(scores)):
            print(f"\n{heads[i]}:")
            zipped = zip(words, scores[i])
            freq = sorted(zipped, key=lambda x: (x[1], x[0]), reverse=True)
            sample = [key for key, val in freq[:10]]
            print(" ".join(sample))

    def main(self):
        self.get_file()


# Uncomment these in case of an error
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('tagsets')
if __name__ == "__main__":
    KTE().main()
