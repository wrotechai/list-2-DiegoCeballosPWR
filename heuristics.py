# heuristics.py


def advance(board, player):
    rows = len(board)
    if rows <= 1:
        return 0.0
    b_score = sum(r for r, row in enumerate(board) for cell in row if cell == 'B') / (rows - 1)
    w_score = sum(rows - 1 - r for r, row in enumerate(board) for cell in row if cell == 'W') / (rows - 1)
    return b_score - w_score if player == 'B' else w_score - b_score


def piece_count(board, player):
    b = sum(cell == 'B' for row in board for cell in row)
    w = sum(cell == 'W' for row in board for cell in row)
    return float(b - w) if player == 'B' else float(w - b)


def threat(board, player):
    rows = len(board)
    threshold = max(1, rows // 2)
    b_threat = sum(
        1 for r in range(rows - threshold, rows)
        for cell in board[r] if cell == 'B'
    )
    w_threat = sum(
        1 for r in range(threshold)
        for cell in board[r] if cell == 'W'
    )
    return float(b_threat - w_threat) if player == 'B' else float(w_threat - b_threat)


def protection(board, player):
    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    def count_protected(piece):
        count = 0
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == piece:
                    for dr in (-1, 1):
                        for dc in (-1, 1):
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == piece:
                                count += 1
                                break
        return count

    b_prot = count_protected('B')
    w_prot = count_protected('W')
    return float(b_prot - w_prot) if player == 'B' else float(w_prot - b_prot)


def adaptive(board, player):
    b_count = sum(cell == 'B' for row in board for cell in row)
    w_count = sum(cell == 'W' for row in board for cell in row)
    total = b_count + w_count
    cols = len(board[0]) if board else 1
    max_pieces = 4 * cols  # 2 starting rows x cols per row x 2 players
    ratio = total / max_pieces if max_pieces > 0 else 1.0

    if ratio > 0.75:
        return 0.5 * protection(board, player) + 0.5 * advance(board, player)
    elif ratio > 0.5:
        return 0.3 * advance(board, player) + 0.7 * threat(board, player)
    else:
        return 0.4 * threat(board, player) + 0.6 * piece_count(board, player)


HEURISTICS = {
    'advance': advance,
    'piece_count': piece_count,
    'threat': threat,
    'protection': protection,
    'adaptive': adaptive,
}
