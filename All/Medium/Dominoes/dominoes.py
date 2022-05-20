# Write your code here
import random


def get_pieces():
    output = []
    for x in range(7):
        for y in range(7):
            piece = [x, y]
            reverse_piece = [y, x]
            if piece not in output and reverse_piece not in output:
                output.append(piece)
    return output


def shuffle(pieces):
    shuffled_pieces = pieces
    length = len(pieces)
    while True:
        random.shuffle(shuffled_pieces)
        _stock = []
        _computer = []
        _player = []
        _snake = []
        first_move = None
        for x in range(length):
            if x < length / 4:
                _computer.append(shuffled_pieces[x])
            elif x < length / 2:
                _player.append(shuffled_pieces[x])
            else:
                _stock.append(shuffled_pieces[x])
        for x in range(6, 0, -1):
            if [x, x] in _player:
                first_move = False
                _snake.append([x, x])
                _player.remove([x, x])
                break
            elif [x, x] in _computer:
                first_move = True
                _snake.append([x, x])
                _computer.remove([x, x])
                break
        if first_move is not None:
            break
    return _stock, _computer, _player, _snake, first_move


def print_game(_sto_p, _com_p, _pla_p, _d_s):
    header = "=" * 70
    print(header)
    print(f"Stock size: {len(_sto_p)}")
    print(f"Computer pieces: {len(_com_p)}\n")
    if len(_d_s) < 6:
        whole_part = _d_s[:6]
        print(*whole_part, sep="")
    else:
        first_part = _d_s[:3]
        second_part = _d_s[-3:]
        print(*first_part, sep="", end="")
        print("...", end="")
        print(*second_part, sep="", end="")
    print(f"\nYour pieces:")
    for x in range(len(_pla_p)):
        print(f"{x + 1}:{_pla_p[x]}")


def print_state(_comp, _pla, _snake, p_turn):
    state = [
        "Computer is about to make a move. Press Enter to continue...",
        "It's your turn to make a move. Enter your command.",
        "The game is over. You won!",
        "The game is over. The computer won!",
        "The game is over. It's a draw!"
    ]
    x = 0
    identical_count = 0
    _game_over = False
    if p_turn is True:
        x = 1
    if len(_pla) == 0:
        x = 2
        _game_over = True
    elif len(_comp) == 0:
        x = 3
        _game_over = True
    elif _snake[0][0] == _snake[-1][1]:
        num = _snake[0][0]
        for i in range(len(_snake)):
            for y in _snake[i]:
                if num == y:
                    identical_count += 1
        if identical_count == 8:
            x = 4
            _game_over = True
    elif p_turn is True:
        x = 1
    print(f"\nStatus: {state[x]}")
    return _game_over


def play_turn(sto_p, com_p, pla_p, snake, p_turn):
    _stock = sto_p
    _computer = com_p
    _player = pla_p
    _snake = snake
    _p_turn = p_turn
    correct_piece = False
    error = "Invalid input. Please try again."
    illegal = "Illegal move. Please try again."
    while True:
        if _p_turn is True:
            i = input()
            left = True if "-" in i else False
            if i.lstrip("-").isdigit():
                i = abs(int(i))
                if i <= len(_player):
                    if i == 0:
                        _player.append(_stock.pop())
                        correct_piece = True
                    elif left:
                        correct_piece = play_piece(i - 1, _player, True, _snake)
                    elif left is False:
                        correct_piece = play_piece(i - 1, _player, False, _snake)
                    if correct_piece:
                        _p_turn = not _p_turn
                        break
                    else:
                        print(illegal)
                else:
                    print(error)
            else:
                print(error)
        else:
            i = input()
            _computer = sort_algorithm(_computer, _snake)
            for x in range(len(_computer)):
                for y in range(2):
                    if correct_piece is False:
                        correct_piece = play_piece(x, _computer, y, _snake)
                    else:
                        break
            if correct_piece:
                _p_turn = not _p_turn
                break
            else:
                _computer.append(_stock.pop())
                _p_turn = not _p_turn
                break
    return _stock, _computer, _player, _snake, _p_turn


def play_piece(index, current_player, left_side, snake):
    done = False
    if left_side:
        for i in range(2):
            if current_player[index][i] == snake[0][0]:
                piece = current_player.pop(index)
                if i == 0:
                    piece = piece[::-1]
                snake.insert(0, piece)
                done = True
                break
    else:
        for i in range(2):
            if current_player[index][i] == snake[-1][1]:
                piece = current_player.pop(index)
                if i == 1:
                    piece = piece[::-1]
                snake.append(piece)
                done = True
                break
    return done

def sort_algorithm(computer, snake):
    new_list = []
    all_list = computer + snake
    scores = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0}
    for x in range(len(all_list)):
        for y in range(2):
            for z in range(7):
                if all_list[x][y] == z:
                    scores[z] += 1
    while len(computer) > 0:
        highest_score = 0
        current_score = 0
        best_piece = []
        for piece in computer:
            for x in piece:
                current_score += scores[x]
            if current_score > highest_score:
                highest_score = current_score
                best_piece = piece
            current_score = 0
        new_list.append(best_piece)
        computer.remove(best_piece)
    return new_list

all_pieces = get_pieces()
stock, computer, player, d_snake, player_turn = shuffle(all_pieces)
game_over = False
while game_over is False:
    print_game(stock, computer, player, d_snake)
    game_over = print_state(computer, player, d_snake, player_turn)
    if game_over:
        break
    stock, computer, player, d_snake, player_turn = \
        play_turn(stock, computer, player, d_snake, player_turn)
