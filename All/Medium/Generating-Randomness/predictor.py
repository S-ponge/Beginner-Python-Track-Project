import re
import random


class RandomnessGenerator:

    def __init__(self):
        self.triads = {
            "000": [0, 0],
            "001": [0, 0],
            "010": [0, 0],
            "011": [0, 0],
            "100": [0, 0],
            "101": [0, 0],
            "110": [0, 0],
            "111": [0, 0]
        }
        self.total_numbers = [0, 0]
        self.max_len = 100
        self.string = ""
        self.test = ""
        self.prediction = ""
        self.running_game = True
        self.balance = 1000

    def take_input(self):
        while len(self.string) < self.max_len:
            i = input("Print a random string containing 0 or 1:\n")
            self.string += re.sub("[^0-1]", "", i)
            if len(self.string) < self.max_len:
                print(f"Current data length is {len(self.string)}, {self.max_len - len(self.string)} symbols left\n")
        print(f"Final data string:\n{self.string}\n")

    def statistics(self):
        for x in self.string:
            if x == "1":
                self.total_numbers[1] += 1
            else:
                self.total_numbers[0] += 1
        self.find_triads()

    def find_triads(self):
        for k, v in self.triads.items():
            occurrences = [i + 3 for i in range(len(self.string)) if self.string.startswith(k, i)]
            for occ in occurrences:
                if occ < len(self.string):
                    if self.string[occ] == "1":
                        v[1] += 1
                    else:
                        v[0] += 1

    def get_test(self):
        i = input("Print a random string containing 0 or 1:\n")
        if i == "enough":
            print("Game over!")
            self.running_game = False
        else:
            self.prediction = ""
            self.test = re.sub("[^0-1]", "", i)
            if self.test != "":
                self.predict()

    def generate_first_triad(self):
        for x in range(3):
            self.prediction += random.choices(["0", "1"], self.total_numbers)[0]

    def predict(self):
        self.generate_first_triad()
        for x in range(len(self.test) - 3):
            triad = self.test[x:x+3]
            freq = self.triads[triad]
            if freq[0] > freq[1]:
                self.prediction += "0"
            elif freq[0] < freq[1]:
                self.prediction += "1"
            else:
                if self.total_numbers[0] > self.total_numbers[1]:
                    self.prediction += "0"
                else:
                    self.prediction += "1"
        print(f"prediction:\n{self.prediction}")
        self.result()

    def result(self):
        correct = 0
        length = len(self.prediction)
        for x in range(3, length):
            if self.prediction[x] == self.test[x]:
                correct += 1
        rate = round((correct / (length - 3)) * 100, 2)
        self.balance -= correct - (length - 3 - correct)
        print(f"Computer guessed right {correct} out of {length - 3} symbols ({rate} %)")
        print(f"Your balance is now ${self.balance}")

    def main(self):
        self.take_input()
        self.statistics()
        while self.running_game:
            self.get_test()


if __name__ == "__main__":
    RandomnessGenerator().main()