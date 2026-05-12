def parse_board(lines):
    return [[cell for cell in line.split()] for line in lines if line.strip()]


def print_board(board):
    for row in board:
        print(' '.join(row))


_EMPTY = {'_', 'o'}


def get_moves(board, player):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    direction = 1 if player == 'B' else -1
    moves = []

    for r in range(rows):
        for c in range(cols):
            if board[r][c] != player:
                continue
            nr = r + direction
            if not (0 <= nr < rows):
                continue
            # Straight forward: only into empty square
            if board[nr][c] in _EMPTY:
                moves.append((r, c, nr, c))
            # Diagonal left: empty or capture (anything except own piece)
            if c - 1 >= 0 and board[nr][c - 1] != player:
                moves.append((r, c, nr, c - 1))
            # Diagonal right: empty or capture
            if c + 1 < cols and board[nr][c + 1] != player:
                moves.append((r, c, nr, c + 1))

    return moves


def apply_move(board, move):
    r_from, c_from, r_to, c_to = move
    rows = len(board)
    cols = len(board[0])
    new_board = [row[:] for row in board]
    piece = new_board[r_from][c_from]
    for r in range(rows):
        for c in range(cols):
            if new_board[r][c] == 'o':
                new_board[r][c] = '_'
    new_board[r_from][c_from] = 'o'
    new_board[r_to][c_to] = piece
    return new_board


def is_terminal(board):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0
    if any(board[rows - 1][c] == 'B' for c in range(cols)):
        return 'B'
    if any(board[0][c] == 'W' for c in range(cols)):
        return 'W'
    return None
