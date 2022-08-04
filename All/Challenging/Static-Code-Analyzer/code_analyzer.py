import sys
import glob
import re
import ast


def search_stylistic_issues(file_dir, lines, ast_tree):
    issue_codes = {"S001": "Too long",
                   "S002": "Indentation is not a multiple of four",
                   "S003": "Unnecessary semicolon",
                   "S004": "At least two spaces required before inline comments",
                   "S005": "TODO found",
                   "S006": "More than two blank lines used before this line",
                   "S007": "Too many spaces after 'class'",
                   "S008": "Class name {} should use CamelCase",
                   "S009": "Function name {} should use snake_case",
                   "S010": "Argument name '{}' should be snake_case",
                   "S011": "Variable '{}' in function should be snake_case",
                   "S012": "Default argument value is mutable"
                   }
    for x in range(len(lines)):
        line = lines[x]
        if line != "":
            comment_index = find_comment(line)
            node = get_ast_object(ast_tree, x + 1)
            for code, message in issue_codes.items():
                if code == "S001":
                    if len(line) > 79:
                        print_error(file_dir, x, code, message)
                elif code == "S002":
                    indent = 0
                    while indent < len(line) and line[indent] == " ":
                        indent += 1
                    if indent > 0 and indent % 4 != 0:
                        print_error(file_dir, x, code, message)
                elif code == "S003":
                    semicolon_index = line.find(";")
                    if semicolon_index != -1:
                        if (comment_index == -1 and line[-1] == ";") or semicolon_index < comment_index:
                            print_error(file_dir, x, code, message)
                elif code == "S004":
                    if comment_index > -1 and comment_index != 0:
                        space_count = 0
                        index = comment_index - 1
                        while line[index] == " ":
                            space_count += 1
                            index -= 1
                        if space_count < 2:
                            print_error(file_dir, x, code, message)
                elif code == "S005":
                    todo_index = line.lower().find("todo")
                    if todo_index != -1 and todo_index > comment_index > -1:
                        print_error(file_dir, x, code, message)
                elif code == "S006":
                    blank_line_count = 0
                    for y in range(1, 4):
                        if lines[x - y] == "":
                            blank_line_count += 1
                    if blank_line_count > 2:
                        print_error(file_dir, x, code, message)
                elif code == "S007":
                    result = find_class_or_function(line)
                    if result is not None and len(result[1]) > 1:
                        print_error(file_dir, x, code, message)
                elif code == "S008":
                    result = find_class_or_function(line)
                    if result is not None and result[0] == "class":
                        pattern = r"^([A-Z][a-z]+)([A-Z][a-z]*)*"
                        name = result[-1]
                        if not re.match(pattern, name):
                            print_error(file_dir, x, code, message.format(name))
                elif code == "S009":
                    result = find_class_or_function(line)
                    if result is not None and result[0] == "def":
                        if not is_snake_case(result[-1].strip("_")):
                            print_error(file_dir, x, code, message.format(result[-1]))
                elif code == "S010" and isinstance(node, ast.FunctionDef):
                    for arg in node.args.args:
                        if not is_snake_case(arg.arg):
                            print_error(file_dir, x, code, message.format(arg.arg))
                elif code == "S011" and isinstance(node, ast.Assign):
                    if hasattr(node.targets[0], "id"):
                        var_name = node.targets[0].id
                        if node.col_offset != 0 and not is_snake_case(var_name):
                            print_error(file_dir, x, code, message.format(var_name))
                elif code == "S012" and isinstance(node, ast.FunctionDef):
                    found_issue = False
                    for default in node.args.defaults:
                        if found_issue is False and not isinstance(default, ast.Constant):
                            found_issue = True
                    if found_issue:
                        print_error(file_dir, x, code, message)


def find_comment(line):  # Todo check if "#" in string
    return line.find("#")


def find_class_or_function(line):
    line = line.lstrip(" ")
    if line.startswith("class"):
        colon_index = line.find(":")
        line = line[:colon_index]
        return re.split(r"(\s+)", line)
    elif line.startswith("def"):
        parenthesis_index = line.find("(")
        line = line[:parenthesis_index]
        return re.split(r"(\s+)", line)
    else:
        return None


def get_ast_object(current_tree, line_number):
    for node in ast.walk(current_tree):
        if hasattr(node, "lineno") and node.lineno == line_number:
            return node


def is_snake_case(name):
    pattern = r"^(?:[a-z]+_)*[a-z-\d]+$"
    if re.match(pattern, name):
        return True
    else:
        return False


def print_error(directory, i, code, message):
    print(f"{directory}: Line {i + 1}: {code} {message}")


if __name__ == "__main__":
    file_name = " ".join(sys.argv[1:])
    if file_name.endswith(".py"):
        with open(file_name, "r", encoding="utf-8") as f:
            lines_list = [line.replace("\n", "") for line in f.readlines()]
            f.seek(0)
            tree = ast.parse(f.read())
            search_stylistic_issues(file_name, lines_list, tree)
    else:
        for file in glob.iglob(f"{file_name}/**/*.py", recursive=True):
            with open(file, "r", encoding="utf-8") as f:
                lines_list = [line.replace("\n", "") for line in f.readlines()]
                f.seek(0)
                tree = ast.parse(f.read())
                search_stylistic_issues(file, lines_list, tree)
