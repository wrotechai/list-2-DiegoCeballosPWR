# agent.py
import time
from minimax import alphabeta, minimax, INF


class Agent:
    def __init__(self, player, heuristic, depth, algorithm='alphabeta'):
        self.player = player
        self.heuristic = heuristic
        self.depth = depth
        self.algorithm = algorithm
        self.nodes_visited = 0
        self.elapsed_ms = 0

    def choose_move(self, board):
        counter = [0]
        start = time.time()
        if self.algorithm == 'minimax':
            _, move = minimax(board, self.player, self.depth, self.heuristic, counter)
        else:
            _, move = alphabeta(board, self.player, self.depth,
                                -INF, INF, self.heuristic, counter)
        self.elapsed_ms += int((time.time() - start) * 1000)
        self.nodes_visited += counter[0]
        return move
