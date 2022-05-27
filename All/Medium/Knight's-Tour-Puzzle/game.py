class Puzzle:
    knight_moves = [
        [2, 1], [2, -1], [-2, 1], [-2, -1],
        [1, 2], [1, -2], [-1, 2], [-1, -2]
    ]

    def __init__(self):
        self.board = [["__" for y in range(8)] for x in range(8)]
        self.label_board = []
        self.board_dimensions = []
        self.cell_size = 0
        self.border_length = 0
        self.knight = [0, 0]
        self.last_move = [0, 0]
        self.first_move = True
        self.total_rounds = 0
        self.computer = False
        self.game_ended = False

    def check_win(self, board, pos, computer=False):
        possible_moves, point = self.get_possible_moves(board, pos)
        win = False
        lose = False
        if len(possible_moves) == 0:
            if self.all_board_filled(board):
                win = True
            else:
                lose = True

            if computer:
                return win, lose
            else:
                if win:
                    print("What a great tour! Congratulations!")
                elif lose:
                    print("No more possible moves!")
                    print(f"Your knight visited {self.total_rounds} squares!")
                self.game_ended = True
        return None, None

    def all_board_filled(self, board):
        filled = True
        for x in range(self.board_dimensions[0] + 1):
            for y in range(self.board_dimensions[1] + 1):
                if not self.is_occupied(board, x, y):
                    filled = False
        return filled

    def clear_board(self, board):
        for x in range(self.board_dimensions[0] + 1):
            for y in range(self.board_dimensions[1] + 1):
                if not self.is_occupied(board, x, y):
                    board[x][y] = "_" * self.cell_size

    def is_occupied(self, board, x, y):
        if board[x][y] == " " * (self.cell_size - 1) + "*":
            return True
        elif board[x][y] == " " * (self.cell_size - 1) + "X":
            return True
        else:
            return False

    def get_possible_moves(self, board, pos, depth=0):
        dim = self.board_dimensions
        possible_moves = []
        total_possible_moves = -1
        for move in self.knight_moves:
            p_move = [pos[0] + move[0], pos[1] + move[1], 0]
            if 0 <= p_move[0] <= dim[0] and 0 <= p_move[1] <= dim[1]:
                if not self.is_occupied(board, p_move[0], p_move[1]):
                    if depth == 0:
                        next_moves, next_total = self.get_possible_moves(board, p_move, depth + 1)
                        p_move[2] = next_total
                    possible_moves.append(p_move)

        total_possible_moves = len(possible_moves) - 1
        return possible_moves, total_possible_moves

    def set_knight_pos(self):
        while True:
            if self.first_move:
                pos = input("Enter the knight's starting position: ").split()
            else:
                pos = input("Enter your next move: ").split()
            if len(pos) == 2 and pos[0].isdigit() and pos[1].isdigit():
                pos = [int(i) - 1 for i in pos]
                x = len(self.board[0]) - 1
                y = len(self.board) - 1
                # print(x, y)
                if 0 <= pos[0] <= x and 0 <= pos[1] <= y:
                    pos.reverse()
                    if not self.is_occupied(self.board, pos[0], pos[1]):
                        if self.first_move:
                            self.first_move = False
                            self.knight = pos
                            break
                        else:
                            l_shaped_move = False
                            for move in self.knight_moves:
                                new_pos = [self.knight[0] + move[0], self.knight[1] + move[1]]
                                if new_pos == pos:
                                    l_shaped_move = True
                            if l_shaped_move:
                                self.knight = pos
                                break
                            else:
                                print("Invalid move!", end=" ")
                    else:
                        print("Invalid move!", end=" ")
                else:
                    print("Invalid position!")
            else:
                print("Invalid position!")

    def move_piece(self, board, label_board, label=1, pos=None, mark_possible=False, reverse=False):
        position = self.knight if pos is None else pos
        mark = "O" if mark_possible else "X"
        moves = []
        if mark_possible:
            self.clear_board(board)
            moves, moves_count = self.get_possible_moves(board, position)
        elif reverse:
            moves.append(position)
        else:
            if not self.first_move:
                self.move_on_board(board, self.last_move[0], self.last_move[1], "*")

            if self.computer:
                moves.append(position)
            else:
                self.set_knight_pos()
                position = self.knight
                self.total_rounds += 1
                moves.append(position)
                self.move_piece(self.board, self.label_board, pos=position, mark_possible=True)

        for move in moves:
            if mark_possible:  # move[2] is total possible moves in that square
                if self.is_occupied(board, move[0], move[1]):
                    pass
                else:
                    self.move_on_board(board, move[0], move[1], move[2])
            else:
                self.move_on_board(board, move[0], move[1], mark)
                self.last_move = [move[0], move[1]]
                self.move_on_board(label_board, move[0], move[1], label)

    def move_on_board(self, board, x, y, mark=None):
        mark = "_" * self.cell_size if mark is None else str(mark)
        board[x][y] = " " * (self.cell_size - len(mark)) + mark

    def set_board(self):
        while True:
            dimensions = input("Enter your board dimensions: ").split()
            if len(dimensions) == 2 and dimensions[0].isdigit() and dimensions[1].isdigit():
                dimensions = [int(i) for i in dimensions]
                if dimensions[0] > 0 and dimensions[1] > 0:
                    self.cell_size = len(str(dimensions[0] * dimensions[1]))
                    self.border_length = dimensions[0] * (self.cell_size + 1) + 3
                    cell = "_" * self.cell_size
                    self.board = [[cell for y in range(dimensions[0])] for x in range(dimensions[1])]
                    self.label_board = [inner[:] for inner in self.board]
                    self.board_dimensions = [dimensions[1] - 1, dimensions[0] - 1]
                    break
                else:
                    print("Invalid dimensions!")
            else:
                print("Invalid dimensions!")

    def set_player_type(self):
        while True:
            i = input("Do you want to try the puzzle? (y/n): ")
            if i == "y":
                self.computer = False
                break
            elif i == "n":
                self.computer = True
                break
            else:
                print("Invalid input!")

    def print_board(self, board):
        bottom_line = "   " + " " * (self.cell_size - 1)
        border = "-" * self.border_length
        num = 1
        print(border)
        for y in range(len(board) - 1, -1, -1):
            print(f"{y + 1}| {' '.join(board[y])} |")
        for x in range(len(board[0])):
            bottom_line += str(num) + " " * self.cell_size
            num += 1
        print(border)
        print(bottom_line)

    def print_solution(self, solved, label_board=None):
        if solved:
            print("Here's the solution!")
            self.print_board(label_board)
        else:
            print("No solution exists!")

    def computer_move(self, board, label_board, old_move, new_move, label, reverse=False):
        if reverse:
            self.move_on_board(board, old_move[0], old_move[1])
            self.move_on_board(board, new_move[0], new_move[1])
            self.move_on_board(label_board, new_move[0], new_move[1])
        else:
            self.move_on_board(board, old_move[0], old_move[1], "*")
            self.move_on_board(board, new_move[0], new_move[1], "X")
            self.move_on_board(label_board, new_move[0], new_move[1], label)

    def computer_mode(self):
        solution_exist, label_board = self.solve(self.board, self.label_board, self.knight)
        return solution_exist, label_board

    def solve(self, board, label_board, pos, label=1):
        new_board = [inner[:] for inner in board]
        new_label_board = [inner[:] for inner in label_board]

        win, lose = self.check_win(new_board, pos, computer=True)
        if win:
            return True, new_label_board
        elif lose:
            return False, new_label_board

        possible_moves, points = self.get_possible_moves(new_board, pos)

        for move in possible_moves:
            self.computer_move(new_board, new_label_board, pos, move, label + 1)
            solution, final_label_board = self.solve(new_board, new_label_board, move, label + 1)
            self.computer_move(new_board, new_label_board, pos, move, label + 1, reverse=True)
            if solution:
                return solution, final_label_board

        return None, None

    def can_solve_puzzle(self):
        self.computer = True
        can_solve, label_board = self.computer_mode()
        self.computer = False
        self.set_player_type()
        if can_solve:
            if self.computer:
                self.print_solution(can_solve, label_board)
                self.game_ended = True
        else:
            self.print_solution(can_solve)
            self.game_ended = True

    def main(self):
        self.set_board()
        self.move_piece(self.board, self.label_board)
        self.can_solve_puzzle()  # Also sets player type if there is a solution
        while not self.game_ended:
            self.print_board(self.board)
            self.check_win(self.board, self.knight)
            if self.game_ended:
                break
            self.move_piece(self.board, self.label_board)


if __name__ == "__main__":
    Puzzle().main()
