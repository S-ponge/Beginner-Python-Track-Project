def check_state(i):
    x_win = 0
    x_count = 0
    o_win = 0
    o_count = 0
    state = False
    for n in range(0, 3):
        if i[n] == i[n + 3] == i[n + 6]:
            if i[n] == "X":
                x_win += 1
            elif i[n] == "O":
                o_win += 1
    for n in range(0, len(i), 3):
        if i[n] == i[n + 1] == i[n + 2]:
            if i[n] == "X":
                x_win += 1
            elif i[n] == "O":
                o_win += 1
    for n in range(0, 3, 2):
        if n == 0:
            if i[n] == i[n + 4] == i[n + 8]:
                if i[n] == "X":
                    x_win += 1
                elif i[n] == "O":
                    o_win += 1
        else:
            if i[n] == i[n + 2] == i[n + 4]:
                if i[n] == "X":
                    x_win += 1
                elif i[n] == "O":
                    o_win += 1
    for n in range(0, len(i)):
        if i[n] == "X":
            x_count += 1
        elif i[n] == "O":
            o_count += 1
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
            print("Game not finished")
    return state


def check_move(coord_text, current_game, turn):
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
                return compare_with_grid(coords[1] - 1, i, turn)
            elif coords[0] == 2:
                return compare_with_grid(coords[0] + coords[1], i, turn)
            else:
                return compare_with_grid(coords[0] * 2 + coords[1] - 1, i, turn)


def compare_with_grid(a, curr, turn_x):
    if curr[a] == "X" or curr[a] == "O":
        print("This cell is occupied! Choose another one!")
        return curr
    else:
        if turn_x is True:
            curr = curr[:a] + "X" + curr[a + 1:]
        else:
            curr = curr[:a] + "O" + curr[a + 1:]
        return curr


def print_game(curr):
    print("---------")
    for n in range(0, len(curr), 3):
        print(f"| {curr[n]} {curr[n + 1]} {curr[n + 2]} |")
    print("---------")


i = "         "
print_game(i)
game_finished = False
x_turn = True
while game_finished is not True:
    old_game = i
    cd = input("Enter the coordinates: ")
    i = check_move(cd, i, x_turn)
    if i == old_game:
        pass
    else:
        print_game(i)
        x_turn = not x_turn
    if check_state(i):
        again = int(input("Press 1 to play again: "))
        if again == 1:
            i = "         "
            print_game(i)
            x_turn = True
        else:
            game_finished = True
