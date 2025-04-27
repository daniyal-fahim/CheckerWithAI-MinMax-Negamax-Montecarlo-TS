from copy import deepcopy
from utils import evaluate_board, is_terminal

def negamax_move(game):
    """Negamax algorithm for AI move."""
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
            # Evaluate the move using negamax with reduced depth and opponent perspective
            score = -negamax(game, temp_board, game.ai_difficulty - 1, -float('inf'), float('inf'), -1)
            # Update best score and move if this move is better
            if score > best_score:
                best_score = score
                best_move = (row, col, move_row, move_col)
    
    # Return the best move found
    return best_move

def negamax(game, board, depth, alpha, beta, color):
    """Negamax with alpha-beta pruning."""
    # Base case: if depth is 0 or the board is in a terminal state, return evaluation adjusted by color
    if depth == 0 or is_terminal(game, board):
        return color * evaluate_board(game, board)
    
    # Initialize maximum score to negative infinity
    max_score = -float('inf')
    # Select piece types based on player (AI: 2, 4; opponent: 1, 3)
    piece_types = (2, 4) if color == 1 else (1, 3)
    # Get all pieces of the current player
    pieces = [(r, c) for r in range(game.board_size) for c in range(game.board_size) if board[r][c] in piece_types]
    
    # Iterate through all pieces
    for row, col in pieces:
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
            # Check if AI piece should be promoted to a king
            if temp_board[move_row][move_col] == 2 and move_row == 0:
                temp_board[move_row][move_col] = 4
            # Check if opponent piece should be promoted to a king
            elif temp_board[move_row][move_col] == 1 and move_row == game.board_size - 1:
                temp_board[move_row][move_col] = 3
            # Recursively evaluate the move from the opponent's perspective
            score = -negamax(game, temp_board, depth - 1, -beta, -alpha, -color)
            # Update maximum score
            max_score = max(max_score, score)
            # Update alpha for pruning
            alpha = max(alpha, score)
            # Alpha-beta pruning: stop evaluating if alpha >= beta
            if alpha >= beta:
                break
    # Return the maximum score
    return max_score