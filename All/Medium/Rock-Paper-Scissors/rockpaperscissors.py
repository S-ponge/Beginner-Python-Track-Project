import random


class RockPaperScissors:
    moves = ["rock", "paper", "scissors"]

    def __init__(self):
        self.player = ""
        self.computer = ""
        self.name = ""
        self.moves = None
        self.index = None
        self.scores = None

    def set_moves(self, moves=None, default=False):
        if default:
            self.moves = ["rock", "paper", "scissors"]
        else:
            self.moves = moves.split(",")

    def set_player_move(self, move):
        self.player = move

    def set_computer_move(self, moves):
        x = random.randint(0, len(moves) - 1)
        self.computer = moves[x]

    def get_index_values(self):
        _moves = self.moves.copy()
        old_index = _moves.index(self.player)
        new_index = len(_moves) // 2 - old_index
        if new_index < 0:
            new_index += len(_moves)
        _moves = _moves[len(_moves) - new_index:len(_moves)] + _moves[:len(_moves) - new_index]
        _player_index = _moves.index(self.player)
        self.set_computer_move(_moves)
        _computer_index = _moves.index(self.computer)
        return _player_index, _computer_index

    def select_winner(self):
        player_index, computer_index = self.get_index_values()
        if player_index > computer_index:
            self.rating(100)
            return f"Well done. The computer chose {self.computer} and failed"
        elif player_index == computer_index:
            self.rating(50)
            return f"There is a draw {self.computer}"
        else:
            return f"Sorry, but the computer chose {self.computer}"

    def rating(self, add_score=0, read_file=False, write_file=False, print_rating=False):
        if read_file:
            with open("rating.txt", "r") as file:
                self.scores = file.readlines()
                self.scores = [score.split() for score in self.scores]
            for score in self.scores:
                if score[0] == self.name:
                    self.index = self.scores.index(score)
            if self.index is None:
                new = [self.name, 0]
                self.scores.append(new)
                self.index = self.scores.index(new)
        elif write_file:
            with open("rating.txt", "w") as file:
                for score in self.scores:
                    print(f"{score[0]} {score[1]}", end="\n", file=file)
        elif print_rating:
            print(f"Your rating: {self.scores[self.index][1]}")
        else:
            curr = int(self.scores[self.index][1])
            self.scores[self.index][1] = str(curr + add_score)

    def main(self):
        end_game = False
        self.name = input("Enter your name: ")
        self.rating(read_file=True)
        print(f"Hello, {self.name}")
        options = input("Enter the moves without space, leave empty for default(rock,paper,scissors):")
        if options == "":
            self.set_moves(default=True)
        else:
            self.set_moves(options)
        input_text = "Enter: "
        for move in self.moves:
            input_text += move + ", "
        input_text += "!rating, !exit:"
        print("Okay, let's start")
        while not end_game:
            option = input(input_text)
            if option in self.moves:
                self.set_player_move(option)
                print(self.select_winner())
            elif option == "!exit":
                self.rating(write_file=True)
                print("Bye!")
                end_game = True
            elif option == "!rating":
                self.rating(print_rating=True)
            else:
                print("Invalid input")


if __name__ == "__main__":
    RockPaperScissors().main()
