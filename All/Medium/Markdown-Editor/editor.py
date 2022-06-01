class MarkdownEditor:

    def __init__(self):
        self.format_commands = {
            "plain": self.plain_format,
            "bold": self.bold_format,
            "italic": self.italic_format,
            "bold-italic": self.bold_italic_format,
            "header": self.header_format,
            "link": self.link_format,
            "inline-code": self.inline_code_format,
            "ordered-list": self.list_format,
            "unordered-list": self.list_format,
            "new-line": self.new_line_format,
        }

        self.special_commands = {
            "!help": self.print_commands,
            "!done": self.exit_editor,
        }

        self.running = True
        self.special_command = False
        self.chosen_command = ""
        self.last_command = ""
        self.text = []
        self.current_text = ""

    def set_command(self):
        while True:
            command = input("Choose a formatter: ")
            if command in self.format_commands:
                self.special_command = False
                self.last_command = self.chosen_command
                self.chosen_command = command
                break
            elif command in self.special_commands:
                self.special_command = True
                self.last_command = self.chosen_command
                self.chosen_command = command
                break
            else:
                print("Unknown formatting type or command")

    def use_command(self):
        if self.special_command:
            self.special_commands[self.chosen_command]()
        else:
            self.format_commands[self.chosen_command]()

    def plain_format(self):
        self.current_text += self.get_text()
        print(self.current_text)

    def bold_format(self):
        self.current_text += f"**{self.get_text()}**"
        print(self.current_text)

    def italic_format(self):
        self.current_text += f"*{self.get_text()}*"
        print(self.current_text)

    def bold_italic_format(self):
        self.current_text += f"***{self.get_text()}***"
        print(self.current_text)

    def inline_code_format(self):
        self.current_text += f"`{self.get_text()}`"
        print(self.current_text)

    def link_format(self):
        if self.current_text:
            self.save_text(self.current_text)
        self.current_text = f"[{self.get_text('Label: ')}]({self.get_text('URL: ')})"
        print(self.current_text)

    def header_format(self):
        if self.current_text:
            self.save_text(self.current_text)
        while True:
            level = int(input("Level: "))
            if level < 1 or level > 6:
                print("The level should be within the range of 1 to 6")
            else:
                break
        self.current_text = f"{'#' * level} {self.get_text()}"
        self.new_line_format()

    def list_format(self):
        ordered = "ordered-list"
        unordered = "unordered-list"
        if self.current_text:
            if self.last_command != ordered and self.last_command != unordered:
                self.save_text(self.current_text)

        while True:
            rows = int(input("Number of rows: "))
            if rows > 0:
                break
            else:
                print("The number of rows should be greater than zero")

        if self.chosen_command == ordered:
            for x in range(1, rows + 1):
                row = input(f'Row #{x} ')
                self.current_text += f"{x}. {row}\n"
        elif self.chosen_command == unordered:
            for x in range(1, rows + 1):
                row = input(f'Row #{x} ')
                self.current_text += f"* {row}\n"
        print(self.current_text)

    def new_line_format(self):
        self.current_text += "\n"
        print(self.current_text)
        self.save_text(self.current_text)

    def print_commands(self):
        print("Available formatters:", " ".join(self.format_commands.keys()))
        print("Special commands:", " ".join(self.special_commands.keys()))

    def print_text(self):
        for line in self.text:
            print(line)

    @staticmethod
    def get_text(require="Text: "):
        line = input(require)
        return line

    def save_text(self, line="\n"):
        self.text.append(line)
        self.current_text = ""

    def save_file(self):
        with open("output.md", mode="w", encoding='utf-8') as file:
            file.writelines(self.text)

    def exit_editor(self):
        if self.current_text:
            self.save_text(self.current_text)
        self.save_file()
        self.running = False

    def main(self):
        while self.running:
            self.set_command()
            self.use_command()


if __name__ == "__main__":
    MarkdownEditor().main()
