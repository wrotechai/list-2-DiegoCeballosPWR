# minimax.py
from board import get_moves, apply_move, is_terminal

INF = float('inf')


def minimax(board, player, depth, heuristic, counter):
    counter[0] += 1
    opponent = 'W' if player == 'B' else 'B'

    winner = is_terminal(board)
    if winner == player:
        return INF, None
    if winner == opponent:
        return -INF, None

    if depth == 0:
        return heuristic(board, player), None

    moves = get_moves(board, player)
    if not moves:
        return heuristic(board, player), None

    best_score = -INF
    best_move = moves[0]

    for move in moves:
        new_board = apply_move(board, move)
        score, _ = minimax(new_board, opponent, depth - 1, heuristic, counter)
        score = -score
        if score > best_score:
            best_score = score
            best_move = move

    return best_score, best_move


def alphabeta(board, player, depth, alpha, beta, heuristic, counter):
    counter[0] += 1
    opponent = 'W' if player == 'B' else 'B'

    winner = is_terminal(board)
    if winner == player:
        return INF, None
    if winner == opponent:
        return -INF, None

    if depth == 0:
        return heuristic(board, player), None

    moves = get_moves(board, player)
    if not moves:
        return heuristic(board, player), None

    best_score = -INF
    best_move = moves[0]

    for move in moves:
        new_board = apply_move(board, move)
        score, _ = alphabeta(new_board, opponent, depth - 1, -beta, -alpha,
                              heuristic, counter)
        score = -score  # negamax: flip perspective
        if score > best_score:
            best_score = score
            best_move = move
        alpha = max(alpha, score)
        if alpha >= beta:
            break

    return best_score, best_move
