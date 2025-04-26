from copy import deepcopy
from utils import evaluate_board, is_terminal

def minimax_move(game):
    """Minimax algorithm for AI move."""
    best_score = -float('inf')
    best_move = None
    ai_pieces = [(r, c) for r in range(game.board_size) for c in range(game.board_size) if game.board[r][c] in (2, 4)]
    
    for row, col in ai_pieces:
        moves = game.get_valid_moves(row, col)
        for move_row, move_col in moves:
            temp_board = deepcopy(game.board)
            temp_board[row][col] = 0
            temp_board[move_row][move_col] = game.board[row][col]
            if abs(row - move_row) == 2:
                captured_row = (row + move_row) // 2
                captured_col = (col + move_col) // 2
                temp_board[captured_row][captured_col] = 0
            if temp_board[move_row][move_col] == 2 and move_row == 0:
                temp_board[move_row][move_col] = 4
            score = minimax(game, temp_board, game.ai_difficulty - 1, -float('inf'), float('inf'), False)
            if score > best_score:
                best_score = score
                best_move = (row, col, move_row, move_col)
    
    return best_move

def minimax(game, board, depth, alpha, beta, maximizing_player):
    """Minimax with alpha-beta pruning."""
    if depth == 0 or is_terminal(game, board):
        return evaluate_board(game, board)
    
    if maximizing_player:
        max_eval = -float('inf')
        for row, col in [(r, c) for r in range(game.board_size) for c in range(game.board_size) if board[r][c] in (2, 4)]:
            moves = game.get_valid_moves_for_board(board, row, col)
            for move_row, move_col in moves:
                temp_board = deepcopy(board)
                temp_board[row][col] = 0
                temp_board[move_row][move_col] = board[row][col]
                if abs(row - move_row) == 2:
                    captured_row = (row + move_row) // 2
                    captured_col = (col + move_col) // 2
                    temp_board[captured_row][captured_col] = 0
                if temp_board[move_row][move_col] == 2 and move_row == 0:
                    temp_board[move_row][move_col] = 4
                eval_score = minimax(game, temp_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for row, col in [(r, c) for r in range(game.board_size) for c in range(game.board_size) if board[r][c] in (1, 3)]:
            moves = game.get_valid_moves_for_board(board, row, col)
            for move_row, move_col in moves:
                temp_board = deepcopy(board)
                temp_board[row][col] = 0
                temp_board[move_row][move_col] = board[row][col]
                if abs(row - move_row) == 2:
                    captured_row = (row + move_row) // 2
                    captured_col = (col + move_col) // 2
                    temp_board[captured_row][captured_col] = 0
                if temp_board[move_row][move_col] == 1 and move_row == game.board_size - 1:
                    temp_board[move_row][move_col] = 3
                eval_score = minimax(game, temp_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
        return min_eval