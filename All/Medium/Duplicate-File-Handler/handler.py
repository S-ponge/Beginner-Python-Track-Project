import operator
import os
import sys
import hashlib
import time
from collections import defaultdict


class DuplicateHandler:

    def __init__(self):
        self.dirs = []
        self.file_sizes = defaultdict(list)
        self.sorted_dict = {}
        self.root_dir = ""
        self.sorting = ""
        self.descending = False
        self.file_format = ""

    def get_root(self):
        # i = input()
        i = args[0] if len(args) >= 1 else ""
        if os.path.isdir(i):
            self.root_dir = i
            self.get_dirs()
        else:
            print("Directory is not specified")

    def get_vars(self):
        sorting_options = ["Descending", "Ascending"]
        file_format = input("(leave empty for all) Enter file format: ")
        if not file_format.startswith(".") and file_format != "":
            self.file_format = "." + file_format
        print("Size sorting options:")
        for x in range(1, 3):
            print(f"{x}. {sorting_options[x - 1]}")
        while True:
            self.sorting = input("Enter a sorting option: ")
            if self.sorting in ["1", "2"]:
                break
            print("Wrong option")
        self.descending = True if self.sorting == "1" else False

    def get_dirs(self):
        for root, dirs, files in os.walk(self.root_dir, True):
            for name in files:
                self.dirs.append(os.path.join(root, name))
            # for name in dirs:
            #     self.dirs.append(os.path.join(root, name))
        self.compare_sizes()

    def compare_sizes(self):
        self.get_vars()
        for file_dir in self.dirs:
            extension = os.path.splitext(file_dir)[-1]
            file_size = os.path.getsize(file_dir)
            if extension == self.file_format or self.file_format == "":
                self.file_sizes[file_size].append(file_dir)
        self.sort_dict()
        self.print_dir(_sorted=True)
        self.check_duplicates()

    def sort_dict(self):
        self.sorted_dict = \
            sorted(self.file_sizes.items(), key=operator.itemgetter(0), reverse=self.descending)

    def check_duplicates(self):
        while True:
            i = input("(yes, no) Check for duplicates? ")
            if i == "yes" or i == "no":
                break
            else:
                print("Wrong option")
        if i == "yes":
            self.print_dir(_sorted=True, check_hash=True)

    def delete_files(self, hash_dict, max_index):
        while True:
            i = input("(yes, no) Delete files? ")
            if i == "yes" or i == "no":
                if i == "yes":
                    while True:
                        numbers = input("Enter file numbers to delete:").split()
                        wrong = False
                        if len(numbers) == 0:
                            wrong = True
                        else:
                            for x in range(len(numbers)):
                                if numbers[x].isdigit():
                                    numbers[x] = int(numbers[x])
                                    if numbers[x] > max_index:
                                        wrong = True
                                else:
                                    wrong = True
                        if not wrong:
                            break
                        else:
                            print("Wrong format")
                break
            else:
                print("Wrong option")
        total_size = 0
        index = 1
        for number in numbers:
            deleted = False
            if not deleted:
                for k, v in hash_dict.items():
                    for file in v:
                        if index == number:
                            total_size += os.path.getsize(file)
                            os.remove(file)
                            index = 1
                            deleted = True
                            break
                        else:
                            index += 1
                    if deleted:
                        break
        print(f"Total freed up space: {total_size} Bytes")

    def get_hash(self, file):
        with open(file, "rb") as f:
            text = f.read()
            md5 = hashlib.md5(text)
            hex_digest = md5.hexdigest()
        return hex_digest

    def print_dir(self, _sorted=False, check_hash=False):
        if not _sorted:
            for name in self.dirs:
                print(name)
        else:
            index = 1
            all_hash_dict = defaultdict(list)
            found_duplicate = False
        for k, v in self.sorted_dict:
            print(f"\n{k} bytes")
            hash_dict = defaultdict(list)
            for file in v:
                if check_hash:
                    file_hash = self.get_hash(file)
                    hash_dict[file_hash].append(file)
                else:
                    print(f"{file}")
            if check_hash:
                for _hash, hash_list in hash_dict.items():
                    if len(hash_list) > 1:
                        print(f"Hash: {_hash}")
                        for hashed in hash_list:
                            all_hash_dict[_hash].append(hashed)
                            found_duplicate = True
                            index_text = f"{index}. "
                            print(f"{index_text}{hashed}")
                            index += 1
        if check_hash:
            if found_duplicate:
                self.delete_files(all_hash_dict, index)
            else:
                print("No duplicate found")


    def main(self):
        self.get_root()


args = sys.argv[1:]
if __name__ == "__main__":
    DuplicateHandler().main()
