class RegexEngine:

    def __init__(self):
        self.running = True
        self.regex = ""
        self.input = ""
        self.special_cases = []  # regex starts with ^ sign or ends with $ sign
        self.metachar_count = 0  # only counts "?" and "*" not "+"

    def get_input(self):
        i = input("type 'regex|test_word' or 'exit': ")
        if i != "exit":
            self.special_cases = []
            self.metachar_count = 0
            self.regex, self.input = i.split("|")
            self.set_vars()
        else:
            self.running = False

    def set_vars(self):
        if self.regex == "":
            print(True)
        elif self.input == "":
            print(False)
        else:
            chars = [char for char in self.input]
            reg = []
            literal_start = False
            literal_end = False
            length = len(self.regex)
            i = 0
            while i < length:
                if self.regex[i] in "?*+\\":
                    if self.regex[i] == "\\" and i < length - 1:
                        if self.regex[i + 1] == "$":
                            literal_end = True
                        elif self.regex[i + 1] == "^":
                            literal_start = True
                        reg.append(self.regex[i + 1])
                        i += 1
                    else:
                        reg[-1] = [reg[-1], self.regex[i]]
                        if self.regex[i] in "?*":
                            self.metachar_count += 1
                else:
                    reg.append(self.regex[i])
                i += 1
            if literal_start is False and reg[0] == "^":
                reg = reg[1:]
                self.special_cases.append("^")
            if literal_end is False and reg[-1] == "$":
                reg = reg[:-1]
                self.special_cases.append("$")
            self.match(reg, chars)

    def match(self, reg, chars):
        match = False
        total = self.metachar_count + len(chars) - len(reg) + 1
        for x in range(total):
            part = chars[x:]
            matched = ""
            if len(part) > 0:
                part_index = 0
                for y in range(len(reg)):
                    if isinstance(reg[y], str):
                        if reg[y] == "." or reg[y] == part[part_index]:
                            matched += part[part_index]
                            match = True
                            part_index += 1
                        else:
                            match = False
                            break
                    else:
                        char, meta_char = reg[y]
                        part_char = part[part_index]
                        if meta_char == "?":
                            if char == part_char:
                                match = True
                                matched += part_char
                                part_index += 1
                            else:
                                match = True
                        else:
                            while part_index < len(part) - 1:
                                if char == "." or char == part_char:
                                    matched += part_char
                                    match = True
                                    part_index += 1
                                    if char == ".":
                                        if y < len(reg) - 1:
                                            while reg[y+1] != part[part_index]:
                                                matched += part[part_index]
                                                if part_index == len(part) - 1:
                                                    break
                                                part_index += 1
                                            break
                                        else:
                                            while part_char == part[part_index]:
                                                matched += part[part_index]
                                                if part_index == len(part) - 1:
                                                    break
                                                part_index += 1
                                            break
                                    else:
                                        while part_char == part[part_index]:
                                            matched += part[part_index]
                                            if part_index == len(part) - 1:
                                                break
                                            part_index += 1
                                        break
                                else:
                                    if meta_char == "*":
                                        match = True
                                        break
            if len(self.special_cases) > 0:
                if "$" in self.special_cases:
                    test = "".join(chars)
                    if not test.endswith(matched):
                        match = False
                if "^" in self.special_cases:
                    if x != 0:
                        break
            if match:
                break
        if match:
            print(True)
        else:
            print(False)

    def main(self):
        while self.running:
            self.get_input()


if __name__ == "__main__":
    RegexEngine().main()
