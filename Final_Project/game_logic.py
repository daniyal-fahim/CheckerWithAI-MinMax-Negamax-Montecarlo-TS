import numpy as np
from copy import deepcopy
from minimax import minimax_move
from negamax import negamax_move
from mcts import mcts_move
from utils import Constants, evaluate_board, is_terminal

class CheckersLogic:
    """Manages the game logic and state for the Checkers game."""
    
    def __init__(self, ai_difficulty, ai_algorithm):
        self.board_size = 8
        self.square_size = 0
        self.board = self.create_initial_board()
        self.current_player = "player"
        self.selected_piece = None
        self.valid_moves = []
        self.game_over = False
        self.move_history = []
        self.ai_difficulty = ai_difficulty
        self.ai_algorithm = ai_algorithm
    
    def create_initial_board(self):
        """Create initial board setup."""
        board = np.zeros((self.board_size, self.board_size), dtype=int)
        for row in range(3):
            for col in range(self.board_size):
                if (row + col) % 2 == 1:
                    board[row][col] = 1  # Player pieces
        for row in range(5, 8):
            for col in range(self.board_size):
                if (row + col) % 2 == 1:
                    board[row][col] = 2  # AI pieces
        return board
    
    def get_valid_moves(self, row, col):
        """Get valid moves for a piece."""
        piece = self.board[row][col]
        moves = []
        captures = []
        
        directions = self.get_directions(piece)
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.board_size and 0 <= c < self.board_size:
                if self.is_opponent_piece(piece, self.board[r][c]):
                    r2, c2 = r + dr, c + dc
                    if 0 <= r2 < self.board_size and 0 <= c2 < self.board_size and self.board[r2][c2] == 0:
                        captures.append((r2, c2))
        
        if captures:
            return captures
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.board_size and 0 <= c < self.board_size and self.board[r][c] == 0:
                moves.append((r, c))
        
        return moves
    
    def get_directions(self, piece):
        """Return valid move directions for a piece."""
        if piece == 1:
            return [(1, -1), (1, 1)]
        elif piece == 2:
            return [(-1, -1), (-1, 1)]
        elif piece in (3, 4):
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return []
    
    def is_opponent_piece(self, piece, other):
        """Check if a piece is an opponent's piece."""
        return (piece in (1, 3) and other in (2, 4)) or (piece in (2, 4) and other in (1, 3))
    
    def make_move(self, from_row, from_col, to_row, to_col, player):
        """Execute a move and update game state."""
        piece = self.board[from_row][from_col]
        self.board[from_row][from_col] = 0
        self.board[to_row][to_col] = piece
        
        if abs(from_row - to_row) == 2:
            captured_row = (from_row + to_row) // 2
            captured_col = (from_col + to_col) // 2
            self.board[captured_row][captured_col] = 0
            
            additional_captures = self.get_valid_moves(to_row, to_col)
            has_additional_captures = any(abs(to_row - r) == 2 for r, c in additional_captures)
            
            if has_additional_captures and self.current_player == "player":
                self.selected_piece = (to_row, to_col)
                self.valid_moves = [move for move in additional_captures if abs(to_row - move[0]) == 2]
                self.move_history.append({
                    'player': player,
                    'from': (from_row, from_col),
                    'to': (to_row, to_col)
                })
                return
        
        if piece == 1 and to_row == self.board_size - 1:
            self.board[to_row][to_col] = 3
        elif piece == 2 and to_row == 0:
            self.board[to_row][to_col] = 4
        
        self.current_player = "ai" if self.current_player == "player" else "player"
        self.move_history.append({
            'player': player,
            'from': (from_row, from_col),
            'to': (to_row, to_col)
        })
        self.check_game_over()
    
    def ai_move(self):
        """Execute AI move based on selected algorithm."""
        import time
        start_time = time.time()
        
        if self.ai_algorithm == "minimax":
            move = minimax_move(self)
        elif self.ai_algorithm == "negamax":
            move = negamax_move(self)
        else:
            move = mcts_move(self)
        
        print(f"AI move time: {time.time() - start_time:.2f}s")
        return move
    
    def get_valid_moves_for_board(self, board, row, col):
        """Get valid moves for a piece on a given board."""
        piece = board[row][col]
        moves = []
        captures = []
        
        directions = self.get_directions(piece)
        for dr, dc in directions:
            r = row + dr
            c = col + dc
            if 0 <= r < self.board_size and 0 <= c < self.board_size:
                if self.is_opponent_piece(piece, board[r][c]):
                    r2 = r + dr
                    c2 = c + dc
                    if 0 <= r2 < self.board_size and 0 <= c2 < self.board_size and board[r2][c2] == 0:
                        captures.append((r2, c2))
        
        if captures:
            return captures
        
        for dr, dc in directions:
            r = row + dr
            c = col + dc
            if 0 <= r < self.board_size and 0 <= c < self.board_size and board[r][c] == 0:
                moves.append((r, c))
        
        return moves
    
    def check_game_over(self):
        """Check for game over conditions."""
        from tkinter import messagebox
        
        player_has_pieces = False
        ai_has_pieces = False
        
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] in (1, 3):
                    player_has_pieces = True
                elif self.board[row][col] in (2, 4):
                    ai_has_pieces = True
        
        if not player_has_pieces:
            self.game_over = True
            messagebox.showinfo("Game Over", "AI wins! You have no pieces left.")  # Updated message
            return
        if not ai_has_pieces:
            self.game_over = True
            messagebox.showinfo("Game Over", "You win! AI has no pieces left.")  # Updated message
            return
        
        if self.current_player == "player":
            has_valid_move = any(self.get_valid_moves(r, c)
                                for r in range(self.board_size) for c in range(self.board_size)
                                if self.board[r][c] in (1, 3))
            if not has_valid_move:
                self.game_over = True
                messagebox.showinfo("Game Over", "AI wins! You have no valid moves.")  # Updated message
                return
        
        elif self.current_player == "ai":
            has_valid_move = any(self.get_valid_moves(r, c)
                                for r in range(self.board_size) for c in range(self.board_size)
                                if self.board[r][c] in (2, 4))
            if not has_valid_move:
                self.game_over = True
                messagebox.showinfo("Game Over", "You win! AI has no valid moves.")  # Updated message
                return