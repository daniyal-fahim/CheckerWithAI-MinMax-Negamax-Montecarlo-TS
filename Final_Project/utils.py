class Constants:
    """Game constants for colors and dimensions."""
    PADDING = 20
    CIRCLE_PADDING = 10
    BOARD_COLOR1 = "#e0c9a6"
    BOARD_COLOR2 = "#5c4033"
    HIGHLIGHT_COLOR = "#81c784"
    PLAYER_COLOR = "#212121"
    AI_COLOR = "#f5f5f5"
    KING_COLOR = "#ffd700"
    VALID_MOVE_COLOR = "#a5d6a7"
    BG_COLOR = "#f5f5f5"

def evaluate_board(game, board):
    """Evaluate board from AI's perspective."""
    ai_score = 0
    player_score = 0
    
    for row in range(game.board_size):
        for col in range(game.board_size):
            piece = board[row][col]
            if piece == 1:
                player_score += 1
                player_score += (game.board_size - 1 - row) * 0.1
            elif piece == 2:
                ai_score += 1
                ai_score += row * 0.1
            elif piece == 3:
                player_score += 1.5
            elif piece == 4:
                ai_score += 1.5
    
    center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
    for row, col in center_squares:
        piece = board[row][col]
        if piece == 1 or piece == 3:
            player_score += 0.2
        elif piece == 2 or piece == 4:
            ai_score += 0.2
    
    return ai_score - player_score

def is_terminal(game, board):
    """Check if board state is terminal."""
    player_pieces = any(board[r][c] in (1, 3) for r in range(game.board_size) for c in range(game.board_size))
    ai_pieces = any(board[r][c] in (2, 4) for r in range(game.board_size) for c in range(game.board_size))
    if not player_pieces or not ai_pieces:
        return True
    
    ai_moves = any(game.get_valid_moves_for_board(board, r, c)
                   for r in range(game.board_size) for c in range(game.board_size) if board[r][c] in (2, 4))
    player_moves = any(game.get_valid_moves_for_board(board, r, c)
                       for r in range(game.board_size) for c in range(game.board_size) if board[r][c] in (1, 3))
    return not ai_moves or not player_moves