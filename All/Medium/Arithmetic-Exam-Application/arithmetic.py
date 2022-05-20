import operator
import random


class Exam:
    operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "**": operator.pow
    }

    def __init__(self):
        self.tasks = {}
        self.level = ""
        self.correct_answers = 0

    def save_result(self):
        i = input("Would you like to save your result to the file? Enter yes or no.").lower()
        if i == "yes" or i == "y":
            name = input("Name?")
            with open("results.txt", "a") as file:
                file.write(f"{name}: {self.correct_answers}/5 in {self.level}\n")
            print('The results are saved in "results.txt".')

    def print_result(self):
        print(f"Your mark is {self.correct_answers}/5")

    def check_answer(self, answer):
        while True:
            try:
                i = float(input())
                if isinstance(answer, int):
                    i = int(i)
                if i == answer:
                    self.correct_answers += 1
                    print("Right!")
                    break
                else:
                    print("Wrong!")
                    break
            except ValueError:
                print("Incorrect format.")

    def start_exam(self):
        for task, answer in self.tasks.items():
            print(task)
            self.check_answer(answer)

    def set_level(self, _operator):
        if _operator == "**":
            self.level = "level 2 (integral squares 11-29)."
        else:
            self.level = "level 1 (simple operations with numbers 2-9)."

    def generate_task(self):
        while True:
            level = input("With the first message, the program should ask for a difficulty level: ")
            if level == "1" or level == "2":
                for x in range(5):
                    while True:
                        if level == "1":
                            while True:
                                a, b = random.choice(list(self.operators.items()))
                                if a != "/" and a != "**":
                                    break
                            x = random.randint(2, 9)
                            y = random.randint(2, 9)
                            task = f"{x} {a} {y}"
                        else:
                            a = "**"
                            b = self.operators.get(a)
                            x = random.randint(11, 29)
                            y = 2
                            task = f"{x}"
                        answer = b(x, y)
                        break
                    self.tasks[task] = answer
                self.set_level(a)
                break
            else:
                print("Incorrect Format.")

    def main(self):
        while True:
            self.generate_task()
            self.start_exam()
            self.print_result()
            self.save_result()
            break


if __name__ == "__main__":
    Exam().main()
