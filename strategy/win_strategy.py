import math

BOARD_SIZE = 3

class Piece:
    EMPTY = 0
    X = 1
    O = 2

def create_doard():
    board = [[Piece.EMPTY for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]
    return board

def game_over(board):
    for i in range(BOARD_SIZE):
        if board[i][0] != Piece.EMPTY and board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            return True

    for j in range(BOARD_SIZE):
        if board[0][j] != Piece.EMPTY and board[0][j] == board[1][j] and board[1][j] == board[2][j]:
            return True

    if board[0][0] != Piece.EMPTY and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return True
    if board[0][2] != Piece.EMPTY and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return True

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == Piece.EMPTY:
                return False
                
    return True

def evaluate(board):
    for i in range(BOARD_SIZE):
        if board[i][0] != Piece.EMPTY and board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            if board[i][0] == Piece.X:
                return 1
            else:
                return -1
                
    for j in range(BOARD_SIZE):
        if board[0][j] != Piece.EMPTY and board[0][j] == board[1][j] and board[1][j] == board[2][j]:
            if board[0][j] == Piece.X:
                return 1
            else:
                return -1
    
    if board[0][0] != Piece.EMPTY and board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        if board[0][0] == Piece.X:
            return 1
        else:
            return -1

    if board[0][2] != Piece.EMPTY and board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        if board[0][2] == Piece.X:
            return 1
        else:
            return -1
    
    return 0

def min_search(board, alpha, beta):
    if game_over(board):
        return evaluate(board)

    min_val = math.inf
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == Piece.EMPTY:
                board[i][j] = Piece.O
                val = max_search(board, alpha, beta)
                min_val = min(min_val, val)
                board[i][j] = Piece.EMPTY
                beta = min(beta, val)
                if beta <= alpha:
                    break
    
    return min_val

def max_search(board, alpha, beta):
    if game_over(board):
        return evaluate(board)

    max_val = -math.inf
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == Piece.EMPTY:
                board[i][j] = Piece.X
                val = min_search(board, alpha, beta)
                max_val = max(max_val, val)
                board[i][j] = Piece.EMPTY
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
                    
    return max_val

def computer_move(board):
    best_val = -math.inf
    best_move = None

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == Piece.EMPTY:
                board[i][j] = Piece.X
                val = min_search(board, -math.inf, math.inf)
                board[i][j] = Piece.EMPTY

                if val > best_val:
                    best_val = val
                    best_move = (i, j)
                
    return best_move

def start_game(ch_flag):
    if ch_flag == 1:
        Piece.X = 2
        Piece.O = 1


if __name__ == "__main__":
    ch_flag = 1
    start_game(ch_flag)
    board = create_doard()
    flag = 0

    print("computer first;player: O,computer: X")
    while not game_over(board):
        row, col = computer_move(board)
        board[row][col] = Piece.X

        print("current board:")
        for row in board:
            print(row)
        
        if game_over(board):
            break

        while True:
            row = int(input("enter row(0-2): "))
            col = int(input("enter col(0-2): "))
            if board[row][col] == Piece.EMPTY:
                board[row][col] = Piece.O
                break
            else:
                print("invalid move")

    print("game over!result:")
    for row in board:
        print(row)
    print("winner:", evaluate(board))
