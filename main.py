# main.py
import argparse
import sys
from board import parse_board, print_board, is_terminal, apply_move
from heuristics import HEURISTICS
from agent import Agent

HEURISTIC_IDS = {'1': 'advance', '2': 'piece_count', '3': 'threat'}


def build_parser():
    parser = argparse.ArgumentParser(description='Breakthrough game')
    parser.add_argument('--algorithm', choices=['minimax', 'alphabeta'], default='alphabeta')
    parser.add_argument('--depth', type=int, default=3,
                        help='Search depth for both players (basic mode)')
    parser.add_argument('--heuristic', default='advance',
                        help='Heuristic name or ID (1, 2, 3) for both players (basic mode)')
    parser.add_argument('--mode', choices=['basic', 'extended'], default='basic')
    parser.add_argument('--depth-b', type=int, default=None,
                        help='Search depth for player B (extended mode)')
    parser.add_argument('--depth-w', type=int, default=None,
                        help='Search depth for player W (extended mode)')
    parser.add_argument('--heuristic-b', default=None)
    parser.add_argument('--heuristic-w', default=None)
    return parser


def run_game(agent_b, agent_w, board):
    agents = {'B': agent_b, 'W': agent_w}
    turn = 'B'
    rounds = 0

    while True:
        winner = is_terminal(board)
        if winner:
            return board, rounds, winner

        move = agents[turn].choose_move(board)
        if move is None:
            winner = 'W' if turn == 'B' else 'B'
            return board, rounds, winner

        board = apply_move(board, move)
        rounds += 1
        turn = 'W' if turn == 'B' else 'B'


def main():
    parser = build_parser()
    args = parser.parse_args()

    lines = sys.stdin.read().splitlines()
    board = parse_board(lines)

    heuristic_key = HEURISTIC_IDS.get(args.heuristic, args.heuristic)

    if args.mode == 'basic':
        h = HEURISTICS[heuristic_key]
        agent_b = Agent('B', h, args.depth, args.algorithm)
        agent_w = Agent('W', h, args.depth, args.algorithm)
    else:
        depth_b = args.depth_b if args.depth_b is not None else args.depth
        depth_w = args.depth_w if args.depth_w is not None else args.depth
        hb_key = HEURISTIC_IDS.get(args.heuristic_b or args.heuristic, args.heuristic_b or heuristic_key)
        hw_key = HEURISTIC_IDS.get(args.heuristic_w or args.heuristic, args.heuristic_w or heuristic_key)
        agent_b = Agent('B', HEURISTICS[hb_key], depth_b, args.algorithm)
        agent_w = Agent('W', HEURISTICS[hw_key], depth_w, args.algorithm)

    final_board, rounds, winner = run_game(agent_b, agent_w, board)

    print_board(final_board)
    print(f"Rounds: {rounds} Winner: {winner}")

    total_nodes = agent_b.nodes_visited + agent_w.nodes_visited
    total_time_s = (agent_b.elapsed_ms + agent_w.elapsed_ms) / 1000.0
    print(total_nodes, file=sys.stderr)
    print(f"{total_time_s:.3f}", file=sys.stderr)


if __name__ == '__main__':
    main()
