import operator
import re


class Calculator:
    operators = {
        "^": [3, operator.pow],
        "*": [2, operator.mul],
        "/": [2, operator.truediv],
        "+": [1, operator.add],
        "-": [1, operator.sub]
    }

    def __init__(self):
        self.op_list = list(self.operators.keys())
        self.operation = "+"
        self.calc_order = []
        self.numbers = {}
        self.variables = {}

    def get_input(self):
        while True:
            i = input()
            if i == "/exit":
                print("Bye!")
                break
            elif i == "/help":
                print("The program calculates the sum of numbers")
            elif i.startswith("/"):
                print("Unknown command")
            elif i == "":
                pass
            else:
                text = self.split_text(i)
                if text is not None:
                    result = self.get_calc_order(text)
                    print(result)

    def split_text(self, text):
        equal_sign = True if "=" in text else False
        pattern = r"([-+*/^]+\.*\s?)" if not equal_sign else r"(=+\s?)"
        s_text = re.split(pattern, text)
        s_text = list(filter(None, [t.strip(" ") for t in s_text]))
        if equal_sign:
            self.add_to_variables(s_text)
        else:
            got_error = False
            x = 0
            while x < len(s_text):
                try:
                    s_text[x] = str(s_text[x])
                    is_negative = False
                    if s_text[x][0] == "-":
                        is_negative = True
                        key = s_text[x].lstrip("-")
                    else:
                        key = s_text[x]
                    if key in self.variables.keys():
                        value = -self.variables[key] if is_negative else self.variables[key]
                        s_text[x] = value
                    else:
                        s_text[x] = int(s_text[x])
                except ValueError:
                    got_error = True
                if isinstance(s_text[x], str):
                    part_len = len(s_text[x])
                    op = s_text[x][0]
                    if op in self.op_list:
                        if s_text[x] == op * part_len:
                            if op in "+-":
                                if x == 0 or s_text[x - 1] in self.op_list:
                                    s_text[x + 1] = op + s_text[x + 1]
                                    del s_text[x]
                                    x -= 1
                                else:
                                    if op == "-" and part_len % 2 == 0:
                                        op = "+"
                                    s_text[x] = op
                                    got_error = False
                            else:
                                if part_len == 1:
                                    s_text[x] = op
                                    got_error = False
                        else:
                            op_2 = s_text[x][1]
                            if part_len == 2 and op_2 == "-" and x != len(s_text):
                                s_text[x] = op
                                s_text[x + 1] = op_2 + s_text[x + 1]
                                got_error = False
                    elif op == "(":
                        result, end_index = self.calculate_parenthesis(s_text[x:], first=True)
                        if result is None:
                            break
                        else:
                            got_error = False
                            s_text[x] = result
                            end_index += x
                            del s_text[x + 1:end_index]
                            x = end_index - x
                x += 1
            if s_text[-1] in self.op_list or got_error:
                if len(s_text) == 1:
                    print("Unknown variable")
                else:
                    print("Invalid expression")
                return None
            else:
                return s_text

    def count_parenthesis(self, parenthesis_list):
        o_count = 0
        c_count = 0
        for x in range(len(parenthesis_list)):
            for char in parenthesis_list[x]:
                counter = 0
                if char == "(":
                    if counter == 0:
                        o_count += 1
                    counter += 1
                elif char == ")":
                    if counter == 0:
                        c_count += 1
                    counter += 1
        if o_count == c_count:
            return True, o_count
        return False

    def calculate_parenthesis(self, text_list, first=False):
        correct_parenthesis = False
        if first:
            correct_parenthesis, o_count = self.count_parenthesis(text_list)
        else:
            correct_parenthesis = True
        if correct_parenthesis:
            parenthesis_list = [text_list[0].strip("(")]
            i = 1
            while i <= len(text_list):
                if text_list[i].startswith("("):
                    result, end_index = self.calculate_parenthesis(text_list[i:])
                    if result is None:
                        break
                    else:
                        parenthesis_list.append(result)
                        end_index = i + end_index
                        del text_list[i + 1:end_index]
                        i = end_index - i
                else:
                    end_p = True if text_list[i].endswith(")") else False
                    parenthesis_list.append(text_list[i].strip(")"))
                    del text_list[i]
                    i -= 1
                if end_p:
                    break
                else:
                    if i == len(text_list):
                        return None, 0
                    i += 1
            parenthesis_list = self.split_text(" ".join([str(p_text) for p_text in parenthesis_list]))
            parenthesis_numbers = {}
            parenthesis_result = self.get_calc_order(parenthesis_list, parenthesis_numbers)
            if first:
                return parenthesis_result, len(parenthesis_list) + o_count
            else:
                return parenthesis_result, len(parenthesis_list)
        return None, 0

    def get_calc_order(self, text, numbers=None):
        if len(text) > 1:
            number_list = self.numbers if numbers is None else numbers
            number_list.clear()
            calc_order = []
            for x in range(len(text)):
                if text[x] in self.op_list:
                    calc = [text[x]]
                    if x == 0:
                        number_list[0] = 0
                        calc.append(0)
                    else:
                        number_list[x - 1] = text[x - 1]
                        calc.append(x - 1)
                    number_list[x + 1] = text[x + 1]
                    calc.append(x + 1)
                    self.add_to_order(calc, calc_order)
            result = self.perform_calc(calc_order, number_list)
            return int(result)
        else:
            return text[0]

    def add_to_order(self, calc, order):
        calc_op = calc[0]
        calc_op_value = self.operators[calc_op][0]
        order_len = len(order)
        if order_len > 0:
            if calc_op_value == 1:
                order.append(calc)
            else:
                not_added = True
                for x in range(len(order)):
                    ordered_op_value = self.operators[order[x][0]][0]
                    if calc_op_value > ordered_op_value:
                        order.insert(x, calc)
                        not_added = False
                        break
                if not_added:
                    order.append(calc)
        else:
            order.append(calc)

    def add_to_variables(self, text):
        errors = [
            "Invalid assignment",
            "Invalid identifier",
            "Unknown variable"
        ]
        pattern = r"^[a-zA-Z]+$"
        if len(text) == 3:
            var_name, var_value = text[0], text[2]
            if re.match(pattern, var_name):
                no_error = True
                if var_value in self.variables.keys():
                    var_value = self.variables[var_value]
                else:
                    try:
                        var_value = int(var_value)
                    except ValueError:
                        no_error = False
                        if re.match(pattern, var_value):
                            print(errors[2])
                        else:
                            print(errors[0])
                if no_error:
                    self.variables[var_name] = var_value
            else:
                print(errors[1])
        else:
            print(errors[0])

    def perform_calc(self, calc_order, numbers):
        total_len = len(calc_order)
        new_variables = {}
        for x in range(total_len):
            calc_op, a, b = calc_order[x]
            if a in new_variables.keys():
                a = new_variables[a]
            else:
                new_variables[a] = b
            if b in new_variables.keys():
                b = new_variables[b]
            else:
                new_variables[b] = b
            calc_result = self.operators[calc_op][1](numbers[a], numbers[b])
            numbers[a] = numbers[b] = calc_result
            if x == total_len - 1:
                return calc_result

    def print_result(self, result):
        print(result)

    def main(self):
        self.get_input()


if __name__ == "__main__":
    Calculator().main()
