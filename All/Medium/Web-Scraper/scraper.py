import requests
import os
from bs4 import BeautifulSoup


class InvalidURLError(Exception):

    def __init__(self, status_code):
        self.status_code = status_code


class Scraper:

    def __init__(self):
        self.current_dir = ""
        self.target_type = ""
        self.total_pages = 0
        self.parameters = {
            "sort": "PubDate",
            "year": 2020,
            "page": 1
        }

    def set_parameters(self):
        self.total_pages = int(input()) + 1
        self.target_type = input()

    def request_link(self, page_link=None):
        site = "https://www.nature.com"
        try:
            if page_link is None:
                url = site + "/nature/articles"
                r = requests.get(url, params=self.parameters)
            else:
                url = site + page_link
                r = requests.get(url)
            if r:
                return BeautifulSoup(r.content, "html.parser")
            else:
                raise InvalidURLError(r.status_code)
        except InvalidURLError as Argument:
            print(f"The URL returned {Argument}!")

    def create_dir(self):
        directory = f"Page_{self.parameters['page']}"
        self.current_dir = os.path.join(os.getcwd(), directory)
        if not os.path.exists(self.current_dir):
            os.mkdir(self.current_dir)

    def save_file(self, name, desc):
        save_name = f"{self.format_name(name)}.txt"
        txt_dir = os.path.join(self.current_dir, save_name)
        with open(txt_dir, "w", encoding="UTF-8") as file:
            file.write(desc)

    @staticmethod
    def format_name(name):
        chars_to_remove = "\\/-—:?*<>|"
        new_name = name
        for char in chars_to_remove:
            new_name = new_name.replace(char, "")
        new_name = new_name.replace("\n", "")
        new_name = new_name.replace(" ", "_")
        return new_name

    def get_content(self):
        link = self.request_link()
        article_types = link.find_all("span", {"class": "c-meta__type"})
        articles = link.find_all("div", {"class": "c-card__body u-display-flex u-flex-direction-column"})
        for x in range(len(article_types)):
            if article_types[x].text == self.target_type:
                sub_link = self.request_link(articles[x].find("a").get("href"))
                article = sub_link.find_all("div", {"class": "c-article-body u-clearfix"})
                article_desc = ""
                for a in article:
                    text = a.text.replace("\n", "")
                    article_desc += text
                article_name = articles[x].find("h3").text
                self.save_file(article_name, article_desc)

    def get_by_page(self):
        for x in range(1, self.total_pages):
            self.parameters["page"] = x
            self.create_dir()
            self.get_content()
        print("Done!")

    def main(self):
        self.set_parameters()
        self.get_by_page()


if __name__ == "__main__":
    Scraper().main()
