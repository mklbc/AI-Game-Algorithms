import time

# Game setup
initial_position = {
    'board': [[' ' for _ in range(3)] for _ in range(3)],
    'current_player': 'player1',
    'winner': None
}

# Performance measurement variables
minimax_node_count = 0
alpha_beta_node_count = 0

def print_board(board):
    for row in board:
        print('|'.join(row))
        print('-' * 5)

def is_terminal(position):
    return position['winner'] is not None or all(cell != ' ' for row in position['board'] for cell in row)

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]
    
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]

    return None

def run_game(strategy, position):
    global minimax_node_count
    global alpha_beta_node_count

    while not is_terminal(position):
        print(f"{position['current_player']}'s turn:")
        print_board(position['board'])

        if position['current_player'] == 'player1':
            valid_input = False
            while not valid_input:
                try:
                    # Get row and column input from user
                    user_input = input("Enter row (0-2) and column (0-2): ")
                    # Split the input into two values
                    row, col = map(int, user_input.split())
                    
                    # Ensure that a valid move is made
                    if position['board'][row][col] == ' ':
                        position['board'][row][col] = 'X'  # Player symbol
                        valid_input = True
                    else:
                        print("Invalid move! The cell is already occupied. Try again.")
                except (ValueError, IndexError):
                    print("Invalid input! Please enter two numbers between 0 and 2 separated by a space.")

        else:
            start_time = time.time()
            if strategy == 'minimax':
                move = minimax(position)
            elif strategy == 'alpha_beta':
                move = alpha_beta_decision(position)
            elapsed_time = time.time() - start_time
            
            position['board'][move[0]][move[1]] = 'O'  # Computer symbol
            print(f"{strategy.capitalize()} chose move: {move}")
            print(f"{strategy.capitalize()} time taken: {elapsed_time:.2f} seconds")
            if strategy == 'minimax':
                print(f"Minimax nodes expanded: {minimax_node_count}")
            elif strategy == 'alpha_beta':
                print(f"Alpha-Beta nodes expanded: {alpha_beta_node_count}")

        position['winner'] = check_winner(position['board'])
        position['current_player'] = 'player2' if position['current_player'] == 'player1' else 'player1'

    print_board(position['board'])
    print(f"The game is over. Winner: {position['winner']}")

def minimax(position):
    global minimax_node_count
    minimax_node_count += 1

    best_score = float('-inf')
    best_move = None

    for i in range(3):
        for j in range(3):
            if position['board'][i][j] == ' ':
                position['board'][i][j] = 'O'  # Computer move
                score = minimax_score(position, False)
                position['board'][i][j] = ' '  # Undo the move

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    return best_move

def minimax_score(position, is_maximizing):
    global minimax_node_count
    minimax_node_count += 1

    winner = check_winner(position['board'])
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    elif is_terminal(position):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for i in range(3):
            for j in range(3):
                if position['board'][i][j] == ' ':
                    position['board'][i][j] = 'O'
                    score = minimax_score(position, False)
                    position['board'][i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if position['board'][i][j] == ' ':
                    position['board'][i][j] = 'X'
                    score = minimax_score(position, True)
                    position['board'][i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

# Alpha-Beta pruning algorithm
def alpha_beta_decision(position):
    global alpha_beta_node_count
    best_move = None
    best_value = float('-inf')

    for i in range(3):
        for j in range(3):
            if position['board'][i][j] == ' ':
                position['board'][i][j] = 'O'  # Computer move
                value = alpha_beta(position, 0, float('-inf'), float('inf'), False)
                position['board'][i][j] = ' '  # Undo the move

                if value > best_value:
                    best_value = value
                    best_move = (i, j)

    return best_move

def alpha_beta(position, depth, alpha, beta, is_maximizing):
    global alpha_beta_node_count
    alpha_beta_node_count += 1

    winner = check_winner(position['board'])
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    elif is_terminal(position):
        return 0

    if is_maximizing:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if position['board'][i][j] == ' ':
                    position['board'][i][j] = 'O'
                    eval = alpha_beta(position, depth + 1, alpha, beta, False)
                    position['board'][i][j] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if position['board'][i][j] == ' ':
                    position['board'][i][j] = 'X'
                    eval = alpha_beta(position, depth + 1, alpha, beta, True)
                    position['board'][i][j] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Start the game flow
if __name__ == "__main__":
    # Ask the user which strategy to choose
    strategy = input("Choose strategy (minimax/alpha_beta): ").strip().lower()
    
    # Check if the strategy is valid
    while strategy not in ['minimax', 'alpha_beta']:
        strategy = input("Invalid strategy! Please choose 'minimax' or 'alpha_beta': ").strip().lower()

    run_game(strategy, initial_position)
