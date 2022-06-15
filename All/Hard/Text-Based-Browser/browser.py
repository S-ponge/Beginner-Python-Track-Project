import os
import sys
import requests
from bs4 import BeautifulSoup as bS
from colorama import Fore


class Browser:

    def __init__(self):
        # self.save_dir = f"{os.getcwd()}\\{args[1]}"
        self.save_dir = f"{os.getcwd()}\\test"  # to test on IDE
        self.saved_files = {}
        self.last_file = 0
        self.current_file = 0
        self.url = ""
        self.header = ""
        self.body = ""
        self.is_running = True

    def create_dir(self):
        if not os.access(self.save_dir, os.F_OK):
            os.mkdir(self.save_dir)

    def get_url(self):
        while True:
            i = input()
            if i == "exit":
                self.is_running = False
                break
            elif i == "back":
                self.back()
            else:
                if "." in i:
                    self.url = "https://" + i
                    self.get_content()
                    break
                else:
                    print("Error: Incorrect URL")

    def get_content(self):
        response = requests.get(self.url)
        soup = bS(response.content, "html.parser")
        lines = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "a", "p", "li"])
        text = []
        for line in lines:
            if line.name == "a":
                link = line.get("href")
            b_line = "BLUE" + line.text + "\n"
            w_line = line.text + "\n"
            if b_line in text:
                pass
            elif w_line in text:
                i = text.index(w_line)
                if link is not None:
                    text[i] = b_line
            else:
                # print(line.get("href"))
                # if line.name == "a":
                #     print(line["href"])
                #     if line.name == "p":
                #         print(line["href"])
                if link is None:
                    text.append(w_line)
                else:
                    text.append(b_line)

        self.save_to_file(text)

    def back(self):
        if self.current_file > 0:
            self.current_file -= 1
            self.print_file()

    def print_file(self):
        file_dir = self.saved_files[self.current_file][1]
        with open(file_dir, "r", encoding="utf-8") as file:
            text = file.readlines()
            for line in text:
                line = line.replace("\n", "")
                if line.startswith("BLUE"):
                    line = line.replace("BLUE", "")
                    print(Fore.BLUE + line)
                else:
                    print(Fore.RESET + line)

    def save_to_file(self, text):
        name = self.url[7:self.url.rfind(".")]  # https:// len is 7
        file_dir = f"{self.save_dir}\\{name}"
        with open(file_dir, "w", encoding="utf-8") as file:
            file.writelines(text)
        self.last_file = len(self.saved_files)
        self.current_file = self.last_file
        self.saved_files[self.last_file] = [name, file_dir]
        self.print_file()

    def main(self):
        self.create_dir()
        while self.is_running:
            self.get_url()


args = sys.argv
if __name__ == "__main__":
    Browser().main()
