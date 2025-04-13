import numpy as np

def evaluate(position):
    """Evaluates the game state."""
    winner = position['winner']
    if winner == 'player1':
        return 10  # Player 1 wins
    elif winner == 'player2':
        return -10  # Player 2 wins
    return 0  # Draw or ongoing game

def get_children(position):
    """Returns all possible child positions from the given position."""
    children = []
    for i in range(3):
        for j in range(3):
            if position['board'][i][j] is None:  # Find an empty cell
                new_board = [row[:] for row in position['board']]
                new_board[i][j] = position['current_player']  # Player makes a move
                winner = check_winner(new_board)
                children.append({
                    'board': new_board,
                    'winner': winner,
                    'moves': position['moves'] + 1,
                    'current_player': 'player2' if position['current_player'] == 'player1' else 'player1'
                })
    return children

def is_terminal(position):
    """Checks if the game has ended."""
    return position['winner'] is not None or position['moves'] == 9

def check_winner(board):
    """Checks for a winner."""
    # Check rows
    for row in board:
        if row[0] is not None and row[0] == row[1] == row[2]:
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] is not None and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]
    
    # Check diagonals
    if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    
    return None  # No winner

def alphabeta(position, depth, alpha, beta, is_maximizing, node_count=0):
    """Applies the Alpha-Beta pruning algorithm."""
    node_count += 1  # Count each node
    if depth == 0 or is_terminal(position):
        return evaluate(position), node_count

    if is_maximizing:
        max_eval = -np.inf
        for child in get_children(position):
            eval, node_count = alphabeta(child, depth - 1, alpha, beta, False, node_count)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Pruning
        return max_eval, node_count
    else:
        min_eval = np.inf
        for child in get_children(position):
            eval, node_count = alphabeta(child, depth - 1, alpha, beta, True, node_count)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Pruning
        return min_eval, node_count
