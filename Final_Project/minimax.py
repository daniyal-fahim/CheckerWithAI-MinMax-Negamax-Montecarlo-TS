from copy import deepcopy
from utils import evaluate_board, is_terminal

def minimax_move(game):
    """Minimax algorithm for AI move."""
    # Initialize best score to negative infinity and best move to None
    best_score = -float('inf')
    best_move = None
    # Get all AI pieces (regular pieces = 2, kings = 4)
    ai_pieces = [(r, c) for r in range(game.board_size) for c in range(game.board_size) if game.board[r][c] in (2, 4)]
    
    # Iterate through all AI pieces
    for row, col in ai_pieces:
        # Get valid moves for the current piece
        moves = game.get_valid_moves(row, col)
        # Iterate through all possible moves for the current piece
        for move_row, move_col in moves:
            # Create a deep copy of the board to simulate the move
            temp_board = deepcopy(game.board)
            # Clear the original position
            temp_board[row][col] = 0
            # Move the piece to the new position
            temp_board[move_row][move_col] = game.board[row][col]
            # Check if the move is a capture (jump)
            if abs(row - move_row) == 2:
                # Calculate the captured piece's position (midpoint)
                captured_row = (row + move_row) // 2
                captured_col = (col + move_col) // 2
                # Remove the captured piece
                temp_board[captured_row][captured_col] = 0
            # Check if the piece should be promoted to a king
            if temp_board[move_row][move_col] == 2 and move_row == 0:
                temp_board[move_row][move_col] = 4
            # Evaluate the move using minimax with reduced depth
            score = minimax(game, temp_board, game.ai_difficulty - 1, -float('inf'), float('inf'), False)
            # Update best score and move if this move is better
            if score > best_score:
                best_score = score
                best_move = (row, col, move_row, move_col)
    
    # Return the best move found
    return best_move

def minimax(game, board, depth, alpha, beta, maximizing_player):
    """Minimax with alpha-beta pruning."""
    # Base case: if depth is 0 or the board is in a terminal state, return evaluation
    if depth == 0 or is_terminal(game, board):
        return evaluate_board(game, board)
    
    # Maximizing player (AI's turn)
    if maximizing_player:
        # Initialize maximum evaluation to negative infinity
        max_eval = -float('inf')
        # Get all AI pieces (regular pieces = 2, kings = 4)
        for row, col in [(r, c) for r in range(game.board_size) for c in range(game.board_size) if board[r][c] in (2, 4)]:
            # Get valid moves for the current piece
            moves = game.get_valid_moves_for_board(board, row, col)
            # Iterate through all possible moves
            for move_row, move_col in moves:
                # Create a deep copy of the board to simulate the move
                temp_board = deepcopy(board)
                # Clear the original position
                temp_board[row][col] = 0
                # Move the piece to the new position
                temp_board[move_row][move_col] = board[row][col]
                # Check if the move is a capture (jump)
                if abs(row - move_row) == 2:
                    # Calculate the captured piece's position (midpoint)
                    captured_row = (row + move_row) // 2
                    captured_col = (col + move_col) // 2
                    # Remove the captured piece
                    temp_board[captured_row][captured_col] = 0
                # Check if the piece should be promoted to a king
                if temp_board[move_row][move_col] == 2 and move_row == 0:
                    temp_board[move_row][move_col] = 4
                # Recursively evaluate the move
                eval_score = minimax(game, temp_board, depth - 1, alpha, beta, False)
                # Update maximum evaluation
                max_eval = max(max_eval, eval_score)
                # Update alpha for pruning
                alpha = max(alpha, eval_score)
                # Alpha-beta pruning: stop evaluating if beta <= alpha
                if beta <= alpha:
                    break
        # Return the maximum evaluation
        return max_eval
    # Minimizing player (opponent's turn)
    else:
        # Initialize minimum evaluation to positive infinity
        min_eval = float('inf')
        # Get all opponent pieces (regular pieces = 1, kings = 3)
        for row, col in [(r, c) for r in range(game.board_size) for c in range(game.board_size) if board[r][c] in (1, 3)]:
            # Get valid moves for the current piece
            moves = game.get_valid_moves_for_board(board, row, col)
            # Iterate through all possible moves
            for move_row, move_col in moves:
                # Create a deep copy of the board to simulate the move
                temp_board = deepcopy(board)
                # Clear the original position
                temp_board[row][col] = 0
                # Move the piece to the new position
                temp_board[move_row][move_col] = board[row][col]
                # Check if the move is a capture (jump)
                if abs(row - move_row) == 2:
                    # Calculate the captured piece's position (midpoint)
                    captured_row = (row + move_row) // 2
                    captured_col = (col + move_col) // 2
                    # Remove the captured piece
                    temp_board[captured_row][captured_col] = 0
                # Check if the piece should be promoted to a king
                if temp_board[move_row][move_col] == 1 and move_row == game.board_size - 1:
                    temp_board[move_row][move_col] = 3
                # Recursively evaluate the move
                eval_score = minimax(game, temp_board, depth - 1, alpha, beta, True)
                # Update minimum evaluation
                min_eval = min(min_eval, eval_score)
                # Update beta for pruning
                beta = min(beta, eval_score)
                # Alpha-beta pruning: stop evaluating if beta <= alpha
                if beta <= alpha:
                    break
        # Return the minimum evaluation
        return min_eval