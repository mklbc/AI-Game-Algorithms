import time
import numpy as np
from minimax1 import minimax
from alphabeta1 import alphabeta

def main():
    initial_position = {
        'board': [[None, None, None], [None, None, None], [None, None, None]],
        'winner': None,
        'moves': 0,
        'current_player': 'player1'  # Start with Player 1
    }

    depth = 3  # Search depth

    # Minimax
    start_time = time.time()
    minimax_result, minimax_node_count = minimax(initial_position, depth, True)
    minimax_duration = time.time() - start_time

    print("Minimax result:", minimax_result)
    print("Minimax execution time (s):", minimax_duration)
    print("Minimax expanded node count:", minimax_node_count)

    # Alpha-Beta
    start_time = time.time()
    alphabeta_result, alphabeta_node_count = alphabeta(initial_position, depth, -np.inf, np.inf, True)
    alphabeta_duration = time.time() - start_time

    print("Alpha-Beta result:", alphabeta_result)
    print("Alpha-Beta execution time (s):", alphabeta_duration)
    print("Alpha-Beta expanded node count:", alphabeta_node_count)

if __name__ == "__main__":
    main()
