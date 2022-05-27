import random


class TicTacToe:
    win_situations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    def __init__(self):
        self.i = "         "
        self.old_state = ""
        self.sides = {"X": "user", "O": "user"}
        self.current_turn = "X"
        self.game_finished = False

    def set_sides(self):
        while True:
            print("Player: user | Bot levels: easy, medium, hard")
            print("Type user or the chosen levels as in the following examples including start")
            print("start user medium | start hard hard | start easy user")
            i = input("> ").split()
            if len(i) != 3:
                if i[0] == "exit":
                    self.game_finished = True
                    break
                else:
                    print("Bad parameters!")
            else:
                self.sides["X"] = i[1]
                self.sides["O"] = i[2]
                break

    def change_turn(self, test_turn=None, test=False):
        if test:
            return "X" if test_turn == "O" else "O"
        else:
            self.current_turn = "X" if self.current_turn == "O" else "O"

    def decide_first_move(self):
        x = 0
        o = 0
        for char in self.i:
            if char == "X":
                x += 1
            elif char == "O":
                o += 1
        if x > o:
            self.current_turn = "O"

    def get_computer_move(self):
        if self.sides[self.current_turn] == "easy":
            self.set_computer_move()
        elif self.sides[self.current_turn] == "medium":
            index_to_play = self.evaluate_state(computer=True)
            if index_to_play is None:
                self.set_computer_move()
            else:
                self.set_computer_move(move=index_to_play, random_move=False)
        elif self.sides[self.current_turn] == "hard":
            index_to_play = self.evaluate_state(computer=True, hard=True)
            self.set_computer_move(index_to_play, random_move=False)

    def set_computer_move(self, move=0, random_move=True):
        print(f'Making move level "{self.sides[self.current_turn]}"')
        while True:
            if random_move:
                random_index = random.randint(0, len(self.i) - 1)
                self.i = self.compare_with_grid(random_index, self.i)
            else:
                self.i = self.compare_with_grid(move, self.i)
            if self.old_state != self.i:
                break

    def empty_index_list(self):
        empty = []
        for x in range(len(self.i)):
            if self.i[x] == " ":
                empty.append(x)
        return empty

    def find_best_move(self):
        best = self.minimax(self.current_turn)
        return best[0]

    def minimax(self, turn, is_maximize=True):

        empty_spots = self.empty_index_list()

        x_win, x_count, o_win, o_count = self.evaluate_state()

        if len(empty_spots) == 0:
            return [0, 0]
        elif x_win > 0:
            if self.current_turn == "X":
                return [0, 10]
            else:
                return [0, -10]
        elif o_win > 0:
            if self.current_turn == "O":
                return [0, 10]
            else:
                return [0, -10]

        moves = []
        for x in empty_spots:
            self.i = self.i[:x] + turn + self.i[x + 1:]
            score = self.minimax(self.change_turn(turn, True), not is_maximize)
            self.i = self.i[:x] + " " + self.i[x + 1:]
            move = [x, score[1]]
            moves.append(move)

        best_move = None
        if turn == self.current_turn:
            best_score = -100
            for move in moves:
                if move[1] > best_score:
                    best_score = move[1]
                    best_move = move[0]
        else:
            best_score = 100
            for move in moves:
                if move[1] < best_score:
                    best_score = move[1]
                    best_move = move[0]

        moves.append([best_move, best_score])
        return moves[-1]

    def evaluate_state(self, test_state=None, computer=False, hard=False):
        i = self.i if test_state is None else test_state
        if computer:
            if hard:
                return self.find_best_move()
            else:
                for situation in self.win_situations:
                    x_in_situation = 0
                    o_in_situation = 0
                    empty_index = None
                    for a in situation:
                        if i[a] == "X":
                            x_in_situation += 1
                        elif i[a] == "O":
                            o_in_situation += 1
                        else:
                            empty_index = a
                    if x_in_situation == 2 or o_in_situation == 2:
                        return empty_index
                return None
        else:
            x_win = 0
            x_count = 0
            o_win = 0
            o_count = 0
            for situation in self.win_situations:
                a, b, c = situation
                if i[a] == i[b] == i[c]:
                    if i[a] == "X":
                        x_win += 1
                    elif i[a] == "O":
                        o_win += 1
            for a in range(len(i)):
                if i[a] == "X":
                    x_count += 1
                elif i[a] == "O":
                    o_count += 1

            return x_win, x_count, o_win, o_count

    def check_state(self):
        state = False
        x_win, x_count, o_win, o_count = self.evaluate_state()
        if x_win > 0:
            if o_win > 0:
                print("Impossible")
            else:
                print("X wins")
                state = True
        elif o_win > 0:
            if x_win > 0:
                print("Impossible")
            else:
                print("O wins")
                state = True
        elif abs(x_count - o_count) > 1:
            print("Impossible")
        elif x_win == 0 and o_win == 0:
            if x_count + o_count == 9:
                print("Draw")
                state = True
            else:
                pass
        return state

    def check_move(self, coord_text, current_game):
        curr = current_game
        coords = []
        for char in coord_text:
            if char.isdigit():
                coords.append(int(char))
        if len(coords) == 0:
            print("You should enter numbers!")
            return curr
        else:
            if coords[0] < 1 or coords[0] > 3 or coords[1] < 0 or coords[1] > 3:
                print("Coordinates should be from 1 to 3!")
                return curr
            else:
                if coords[0] == 1:
                    return self.compare_with_grid(coords[1] - 1, self.i)
                elif coords[0] == 2:
                    return self.compare_with_grid(coords[0] + coords[1], self.i)
                else:
                    return self.compare_with_grid(coords[0] * 2 + coords[1] - 1, self.i)

    def compare_with_grid(self, a, curr, for_testing=False):
        if curr[a] == "X" or curr[a] == "O":
            if self.sides[self.current_turn] == "user":
                print("This cell is occupied! Choose another one!")
            return curr
        else:
            if for_testing:
                test = curr[:a] + self.current_turn + curr[a + 1:]
                return test
            else:
                curr = curr[:a] + self.current_turn + curr[a + 1:]
                return curr

    @staticmethod
    def print_game(curr):
        print("---------")
        for n in range(0, len(curr), 3):
            print(f"| {curr[n]} {curr[n + 1]} {curr[n + 2]} |")
        print("---------")

    def main(self):
        self.set_sides()
        self.print_game(self.i)
        while self.game_finished is not True:
            self.old_state = self.i
            if self.sides[self.current_turn] == "user":
                cd = input("Enter the coordinates: ")
                self.i = self.check_move(cd, self.i)
            else:
                self.get_computer_move()
            if self.i == self.old_state:
                pass
            else:
                self.print_game(self.i)
                self.change_turn()
            if self.check_state():
                self.change_turn()
                self.game_finished = True


if __name__ == "__main__":
    TicTacToe().main()
