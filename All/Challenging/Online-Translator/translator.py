import os
import sys
import requests
from bs4 import BeautifulSoup
import re


class Translator:

    def __init__(self):
        self.header = {'User-Agent': 'Mozilla/5.0'}
        self.languages = {1: "English", 2: "German", 3: "Turkish", 4: "Spanish", 5: "French",
                          6: "Dutch", 7: "Portuguese", 8: "Italian", 9: "Japanese", 10: "Hebrew",
                          11: "Polish", 12: "Russian", 13: "Romanian", 14: "Arabic"}
        self.all = False
        self.chosen_langs = []
        self.word = ""
        # self.sentence = []  # Sentence translation can be added later
        self.file_path = ""

    def welcome(self):
        print("Hello, welcome to the translator. Translator supports: ")
        for k, v in self.languages.items():
            print(f"{k}. {v}")

    def get_source_target_language(self):
        unsupported = ""
        for lang in args[0:2]:
            test = lang.capitalize()
            if test != "All" and test not in self.languages.values():
                unsupported = lang
                break
            else:
                self.chosen_langs.append(test)
        if unsupported == "":
            if self.chosen_langs[1] == "All":
                self.all = True
            else:
                self.all = False
            self.get_source_text()
        else:
            print(f"Sorry, the program doesn't support {unsupported}")

    def get_source_text(self):
        self.word = args[2]
        self.perform_translate()

    def perform_translate(self):
        s_l = self.chosen_langs[0].lower()
        connected = True
        if not self.all:
            t_l = self.chosen_langs[1].lower()
            if connected:
                connected = self.translate(s_l, t_l)
        else:
            for k, v in self.languages.items():
                if v not in self.chosen_langs and connected:
                    t_l = v.lower()
                    connected = self.translate(s_l, t_l)
        self.print_file()

    def translate(self, s, t):
        soup = self.get_soup(s, t)
        if isinstance(soup, str):
            print(soup)
            return False
        else:
            lang = t.capitalize()
            self.print_words(soup, lang, 1)  # Change translation count default=1
            self.print_examples(soup, lang, 1)  # Change example count default=1
            return True

    def get_soup(self, s_l, t_l):
        url = f"https://context.reverso.net/translation/{s_l}-{t_l}/{self.word}"
        soup = None
        try:
            page = requests.get(url, headers=self.header)
            if page.status_code == 200:
                soup = BeautifulSoup(page.content, "html.parser")
            elif page.status_code == 404:
                soup = f"Sorry, unable to find {self.word}"
        except requests.exceptions.RequestException:
            soup = "Something wrong with your internet connection"
        return soup

    def print_words(self, soup, lang, counter=10):
        word_gender_dict = soup.find_all(class_=re.compile("translation rtl|ltr dict"))
        words = []
        genders = []
        for item in word_gender_dict:
            wg_list = item.get_text().split()
            words.append(wg_list[0])
            if len(wg_list) > 1:
                genders.append(wg_list[1])
            else:
                genders.append("")
        self.print_both(f"{lang} Translations:")
        for i in range(len(words)):
            if counter > 0:
                if genders[i] != "":
                    self.print_both(f"{words[i]} {genders[i]}")
                else:
                    self.print_both(f"{words[i]}")
                counter -= 1
            else:
                break

    def print_examples(self, soup, lang, counter=10):
        zipped = self.format_zipped(soup)
        self.print_both(f"\n{lang} Example:")
        for (s, t) in zipped:
            if counter > 0:
                self.print_both(s)
                self.print_both(t + "\n")
                counter -= 1
            else:
                break

    def format_zipped(self, soup):
        s_e = [word.text for word in soup.find_all(class_=re.compile("^src"))]
        t_e = [word.text for word in soup.find_all(class_=re.compile("^trg"))]
        for text in s_e:
            i = s_e.index(text)
            text = text.strip()
            text = re.sub(r"[\n\r]", "", text)
            s_e[i] = text
        for text in t_e:
            i = t_e.index(text)
            text = text.strip()
            text = re.sub(r"[\n\r]", "", text)
            t_e[i] = text
        s_e = [i for i in s_e if i]
        t_e = [i for i in t_e if i]
        result = zip(s_e, t_e)
        return result

    def print_both(self, text):  # writes to file while printing
        print(text)
        self.file_path = f"{self.chosen_langs[0]}_{self.word}.txt"
        with open(self.file_path, "a+", encoding="utf-8") as file:
            if os.path.getsize(self.file_path) == 0:
                file.write(text)
            else:
                file.write("\n" + text)

    def print_file(self):
        if self.file_path != "":
            with open(self.file_path, "r", encoding="utf-8") as file:
                print(file.read())

    def main(self):
        self.get_source_target_language()


args = sys.argv[1:]  # Comment to use IDE
# args = ["english", "all", "example"]  # You can also put your inputs here and uncomment
if __name__ == "__main__":
    Translator().main()
