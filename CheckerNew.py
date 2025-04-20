import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import time
from copy import deepcopy

class CheckersGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Checkers Game with AI")
        self.master.geometry("600x700")
        self.master.minsize(400, 500)
        
        # Game settings (will be set by start screen)
        self.player_name = ""
        self.ai_difficulty = 3  # Default medium difficulty
        
        # Show start screen first
        self.show_start_screen()
    
    def show_start_screen(self):
        """Show the start screen with name entry and difficulty selection."""
        self.start_frame = tk.Frame(self.master, padx=20, pady=20)
        self.start_frame.pack(expand=True, fill=tk.BOTH)
        
        # Title
        title_label = tk.Label(
            self.start_frame, 
            text="Checkers Game", 
            font=("Arial", 24, "bold"),
            pady=20
        )
        title_label.pack()
        
        # Name entry
        name_frame = tk.Frame(self.start_frame)
        name_frame.pack(pady=10)
        
        tk.Label(name_frame, text="Your Name:", font=("Arial", 12)).pack(side=tk.LEFT)
        self.name_entry = tk.Entry(name_frame, font=("Arial", 12))
        self.name_entry.pack(side=tk.LEFT, padx=10)
        self.name_entry.focus()
        
        # Difficulty selection
        diff_frame = tk.Frame(self.start_frame)
        diff_frame.pack(pady=10)
        
        tk.Label(diff_frame, text="AI Difficulty:", font=("Arial", 12)).pack(side=tk.LEFT)
        
        self.difficulty = tk.StringVar(value="medium")
        difficulties = [
            ("Easy", "easy"),
            ("Medium", "medium"),
            ("Hard", "hard")
        ]
        
        for text, mode in difficulties:
            rb = tk.Radiobutton(
                diff_frame, 
                text=text, 
                variable=self.difficulty,
                value=mode,
                font=("Arial", 10)
            )
            rb.pack(side=tk.LEFT, padx=5)
        
        # Start button
        start_button = tk.Button(
            self.start_frame,
            text="Start Game",
            command=self.start_game,
            font=("Arial", 12),
            padx=20,
            pady=5,
            bg="#4CAF50",
            fg="white"
        )
        start_button.pack(pady=20)
        
        # Center all widgets
        for child in self.start_frame.winfo_children():
            child.pack_configure(anchor=tk.CENTER)
    
    def start_game(self):
        """Start the game with the selected settings."""
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            messagebox.showwarning("Input Error", "Please enter your name")
            return
        
        # Set AI difficulty
        difficulty_map = {
            "easy": 2,
            "medium": 3,
            "hard": 4
        }
        self.ai_difficulty = difficulty_map[self.difficulty.get()]
        
        # Remove start screen
        self.start_frame.destroy()
        
        # Initialize game
        self.init_game()
    
    def init_game(self):
        """Initialize the game after start screen."""
        # Game constants
        self.BOARD_SIZE = 8
        self.PADDING = 20
        self.CIRCLE_PADDING = 10
        
        # Colors
        self.BOARD_COLOR1 = "#DDB88C"
        self.BOARD_COLOR2 = "#A66D4F"
        self.HIGHLIGHT_COLOR = "#4CAF50"
        self.PLAYER_COLOR = "#333333"  # Dark (black)
        self.AI_COLOR = "#F5F5F5"      # Light (white)
        self.KING_COLOR = "#FFD700"    # Gold for kings
        self.VALID_MOVE_COLOR = "#8BC34A"
        
        # Game state
        self.board = self.create_initial_board()
        self.current_player = "player"  # player or ai
        self.selected_piece = None
        self.valid_moves = []
        self.game_over = False
        
        # AI settings
        self.ai_depth = self.ai_difficulty  # Depth for Minimax algorithm
        
        # Create GUI
        self.create_widgets()
        self.draw_board()
        
        # Start game
        self.update_status()
    
    def create_widgets(self):
        # Main frame with responsive design
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top frame for status
        self.top_frame = tk.Frame(self.main_frame)
        self.top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Status label
        self.status_label = tk.Label(
            self.top_frame,
            text="",
            font=("Arial", 12),
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Difficulty indicator
        diff_text = f"Difficulty: {self.difficulty.get().capitalize()}"
        self.diff_label = tk.Label(
            self.top_frame,
            text=diff_text,
            font=("Arial", 10),
            fg="gray"
        )
        self.diff_label.pack(side=tk.RIGHT)
        
        # Canvas container for responsive board
        self.canvas_container = tk.Frame(self.main_frame)
        self.canvas_container.pack(fill=tk.BOTH, expand=True)
        self.canvas_container.grid_rowconfigure(0, weight=1)
        self.canvas_container.grid_columnconfigure(0, weight=1)
        
        # Canvas for the board (will be resized by update_board_size)
        self.canvas = tk.Canvas(
            self.canvas_container, 
            bg="#F0F0F0",
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_square_clicked)
        self.master.bind("<Configure>", self.on_window_resize)
        
        # Calculate initial board size
        self.update_board_size()
    
    def update_board_size(self, event=None):
        """Update the board size based on current window dimensions."""
        # Get available space
        container_width = self.canvas_container.winfo_width()
        container_height = self.canvas_container.winfo_height()
        
        # Calculate square size to fit the board
        max_square_width = (container_width - 2 * self.PADDING) // self.BOARD_SIZE
        max_square_height = (container_height - 2 * self.PADDING) // self.BOARD_SIZE
        self.SQUARE_SIZE = min(max_square_width, max_square_height)
        
        # Ensure square size is at least 10px
        self.SQUARE_SIZE = max(10, self.SQUARE_SIZE)
        
        # Calculate total board size
        board_width = self.BOARD_SIZE * self.SQUARE_SIZE + 2 * self.PADDING
        board_height = self.BOARD_SIZE * self.SQUARE_SIZE + 2 * self.PADDING
        
        # Update canvas size
        self.canvas.config(width=board_width, height=board_height)
        
        # Redraw board
        self.draw_board()
    
    def on_window_resize(self, event):
        """Handle window resize events."""
        if hasattr(self, 'canvas_container'):
            self.update_board_size()
    
    def create_initial_board(self):
        """Create the initial board setup."""
        board = np.zeros((self.BOARD_SIZE, self.BOARD_SIZE), dtype=int)
        
        # Set up player pieces (top three rows)
        for row in range(3):
            for col in range(self.BOARD_SIZE):
                if (row + col) % 2 == 1:
                    board[row][col] = 1  # 1 represents player's regular piece
        
        # Set up AI pieces (bottom three rows)
        for row in range(5, 8):
            for col in range(self.BOARD_SIZE):
                if (row + col) % 2 == 1:
                    board[row][col] = 2  # 2 represents AI's regular piece
        
        return board
    
    def draw_board(self):
        """Draw the checkerboard and pieces."""
        self.canvas.delete("all")
        
        # Draw squares
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                x1 = self.PADDING + col * self.SQUARE_SIZE
                y1 = self.PADDING + row * self.SQUARE_SIZE
                x2 = x1 + self.SQUARE_SIZE
                y2 = y1 + self.SQUARE_SIZE
                
                # Alternate square colors
                color = self.BOARD_COLOR1 if (row + col) % 2 == 0 else self.BOARD_COLOR2
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
                
                # Highlight selected piece
                if self.selected_piece and self.selected_piece == (row, col):
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2, 
                        fill=self.HIGHLIGHT_COLOR, 
                        outline=self.HIGHLIGHT_COLOR
                    )
                
                # Highlight valid moves
                if (row, col) in self.valid_moves:
                    self.canvas.create_oval(
                        x1 + self.SQUARE_SIZE//4, y1 + self.SQUARE_SIZE//4,
                        x2 - self.SQUARE_SIZE//4, y2 - self.SQUARE_SIZE//4,
                        fill=self.VALID_MOVE_COLOR, outline=self.VALID_MOVE_COLOR
                    )
        
        # Draw pieces
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = self.board[row][col]
                if piece != 0:
                    self.draw_piece(row, col, piece)
    
    def draw_piece(self, row, col, piece):
        """Draw a game piece at the specified position."""
        x1 = self.PADDING + col * self.SQUARE_SIZE + self.CIRCLE_PADDING
        y1 = self.PADDING + row * self.SQUARE_SIZE + self.CIRCLE_PADDING
        x2 = x1 + (self.SQUARE_SIZE - 2 * self.CIRCLE_PADDING)
        y2 = y1 + (self.SQUARE_SIZE - 2 * self.CIRCLE_PADDING)
        
        # Determine piece color and type
        if piece == 1:  # Player regular piece
            color = self.PLAYER_COLOR
            king = False
        elif piece == 2:  # AI regular piece
            color = self.AI_COLOR
            king = False
        elif piece == 3:  # Player king
            color = self.PLAYER_COLOR
            king = True
        elif piece == 4:  # AI king
            color = self.AI_COLOR
            king = True
        
        # Draw the piece
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="#555555", width=2)
        
        # Add crown for kings
        if king:
            crown_x = (x1 + x2) / 2
            crown_y = (y1 + y2) / 2
            self.canvas.create_text(
                crown_x, crown_y, 
                text="♛", 
                fill=self.KING_COLOR, 
                font=("Arial", max(10, int(self.SQUARE_SIZE/5))), 
                anchor=tk.CENTER
            )
    
    def on_square_clicked(self, event):
        """Handle click events on the board."""
        if self.game_over or self.current_player != "player":
            return
        
        # Get clicked position
        col = (event.x - self.PADDING) // self.SQUARE_SIZE
        row = (event.y - self.PADDING) // self.SQUARE_SIZE
        
        # Check if click is outside the board
        if not (0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE):
            return
        
        # If no piece is selected, select one if it's the player's
        if self.selected_piece is None:
            piece = self.board[row][col]
            if piece in (1, 3):  # Player's piece or king
                self.selected_piece = (row, col)
                self.valid_moves = self.get_valid_moves(row, col)
                self.draw_board()
        else:
            # If a piece is already selected, try to move it
            selected_row, selected_col = self.selected_piece
            if (row, col) in self.valid_moves:
                self.make_move(selected_row, selected_col, row, col)
                self.selected_piece = None
                self.valid_moves = []
                self.draw_board()
                
                # Switch to AI turn
                if not self.game_over and self.current_player == "ai":
                    self.master.after(500, self.ai_move)
            else:
                # Clicked on another of player's pieces - select it instead
                piece = self.board[row][col]
                if piece in (1, 3):
                    self.selected_piece = (row, col)
                    self.valid_moves = self.get_valid_moves(row, col)
                    self.draw_board()
    
    def get_valid_moves(self, row, col):
        """Get all valid moves for a piece at (row, col)."""
        piece = self.board[row][col]
        moves = []
        captures = []
        
        # Determine piece type and movement directions
        if piece == 1:  # Player regular piece (moves downward)
            directions = [(1, -1), (1, 1)]
        elif piece == 2:  # AI regular piece (moves upward)
            directions = [(-1, -1), (-1, 1)]
        elif piece in (3, 4):  # Kings (can move in all directions)
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        # Check for captures first (mandatory capture rule)
        for dr, dc in directions:
            # Check if adjacent square has opponent's piece
            r, c = row + dr, col + dc
            if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                if (piece in (1, 3) and self.board[r][c] in (2, 4)) or \
                   (piece in (2, 4) and self.board[r][c] in (1, 3)):
                    # Check if landing square is empty
                    r2, c2 = r + dr, c + dc
                    if 0 <= r2 < self.BOARD_SIZE and 0 <= c2 < self.BOARD_SIZE and self.board[r2][c2] == 0:
                        captures.append((r2, c2))
        
        if captures:
            return captures
        
        # If no captures, check for regular moves
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and self.board[r][c] == 0:
                moves.append((r, c))
        
        return moves
    
    def make_move(self, from_row, from_col, to_row, to_col):
        """Move a piece and handle captures and king promotion."""
        piece = self.board[from_row][from_col]
        self.board[from_row][from_col] = 0
        self.board[to_row][to_col] = piece
        
        # Handle captures
        if abs(from_row - to_row) == 2:  # It's a capture
            captured_row = (from_row + to_row) // 2
            captured_col = (from_col + to_col) // 2
            self.board[captured_row][captured_col] = 0
            
            # Check for additional captures (multi-jump)
            additional_captures = self.get_valid_moves(to_row, to_col)
            has_additional_captures = any(abs(to_row - r) == 2 for r, c in additional_captures)
            
            if has_additional_captures and self.current_player == "player":
                self.selected_piece = (to_row, to_col)
                self.valid_moves = [move for move in additional_captures if abs(to_row - move[0]) == 2]
                self.draw_board()
                return  # Player must continue capturing
        
        # Promote to king if reached the opposite end
        if piece == 1 and to_row == self.BOARD_SIZE - 1:  # Player piece reaches AI's home row
            self.board[to_row][to_col] = 3  # Promote to king
        elif piece == 2 and to_row == 0:  # AI piece reaches player's home row
            self.board[to_row][to_col] = 4  # Promote to king
        
        # Switch player
        self.current_player = "ai" if self.current_player == "player" else "player"
        
        # Check for game over
        self.check_game_over()
        self.update_status()
    
    def ai_move(self):
        """Let the AI make a move using Minimax algorithm."""
        if self.game_over or self.current_player != "ai":
            return
        
        # Get all possible moves for AI
        best_move = None
        best_score = -float('inf')
        
        # Find all AI pieces
        ai_pieces = []
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] in (2, 4):  # AI pieces
                    ai_pieces.append((row, col))
        
        # Evaluate all possible moves for all pieces
        for row, col in ai_pieces:
            moves = self.get_valid_moves(row, col)
            for move_row, move_col in moves:
                # Make a copy of the board to simulate the move
                temp_board = deepcopy(self.board)
                temp_board[row][col] = 0
                temp_board[move_row][move_col] = self.board[row][col]
                
                # Handle captures
                if abs(row - move_row) == 2:
                    captured_row = (row + move_row) // 2
                    captured_col = (col + move_col) // 2
                    temp_board[captured_row][captured_col] = 0
                
                # Handle promotion
                if temp_board[move_row][move_col] == 2 and move_row == 0:
                    temp_board[move_row][move_col] = 4
                
                # Evaluate the move
                score = self.minimax(temp_board, self.ai_depth - 1, -float('inf'), float('inf'), False)
                
                if score > best_score:
                    best_score = score
                    best_move = (row, col, move_row, move_col)
        
        # Make the best move
        if best_move:
            from_row, from_col, to_row, to_col = best_move
            self.make_move(from_row, from_col, to_row, to_col)
            self.draw_board()
        
        # If no valid moves found (shouldn't happen if game isn't over)
        else:
            self.current_player = "player"
            self.update_status()
    
    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """Minimax algorithm with alpha-beta pruning."""
        if depth == 0:
            return self.evaluate_board(board)
        
        if maximizing_player:  # AI's turn
            max_eval = -float('inf')
            
            # Find all AI pieces
            ai_pieces = []
            for row in range(self.BOARD_SIZE):
                for col in range(self.BOARD_SIZE):
                    if board[row][col] in (2, 4):  # AI pieces
                        ai_pieces.append((row, col))
            
            # Evaluate all possible moves
            for row, col in ai_pieces:
                moves = self.get_valid_moves_for_board(board, row, col)
                for move_row, move_col in moves:
                    # Make a copy of the board to simulate the move
                    temp_board = deepcopy(board)
                    temp_board[row][col] = 0
                    temp_board[move_row][move_col] = board[row][col]
                    
                    # Handle captures
                    if abs(row - move_row) == 2:
                        captured_row = (row + move_row) // 2
                        captured_col = (col + move_col) // 2
                        temp_board[captured_row][captured_col] = 0
                    
                    # Handle promotion
                    if temp_board[move_row][move_col] == 2 and move_row == 0:
                        temp_board[move_row][move_col] = 4
                    
                    # Recursive evaluation
                    eval_score = self.minimax(temp_board, depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break  # Beta cutoff
            
            return max_eval
        
        else:  # Player's turn
            min_eval = float('inf')
            
            # Find all player pieces
            player_pieces = []
            for row in range(self.BOARD_SIZE):
                for col in range(self.BOARD_SIZE):
                    if board[row][col] in (1, 3):  # Player pieces
                        player_pieces.append((row, col))
            
            # Evaluate all possible moves
            for row, col in player_pieces:
                moves = self.get_valid_moves_for_board(board, row, col)
                for move_row, move_col in moves:
                    # Make a copy of the board to simulate the move
                    temp_board = deepcopy(board)
                    temp_board[row][col] = 0
                    temp_board[move_row][move_col] = board[row][col]
                    
                    # Handle captures
                    if abs(row - move_row) == 2:
                        captured_row = (row + move_row) // 2
                        captured_col = (col + move_col) // 2
                        temp_board[captured_row][captured_col] = 0
                    
                    # Handle promotion
                    if temp_board[move_row][move_col] == 1 and move_row == self.BOARD_SIZE - 1:
                        temp_board[move_row][move_col] = 3
                    
                    # Recursive evaluation
                    eval_score = self.minimax(temp_board, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break  # Alpha cutoff
            
            return min_eval
    
    def get_valid_moves_for_board(self, board, row, col):
        """Get valid moves for a piece on a given board state."""
        piece = board[row][col]
        moves = []
        captures = []
        
        # Determine piece type and movement directions
        if piece == 1:  # Player regular piece (moves downward)
            directions = [(1, -1), (1, 1)]
        elif piece == 2:  # AI regular piece (moves upward)
            directions = [(-1, -1), (-1, 1)]
        elif piece in (3, 4):  # Kings (can move in all directions)
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        # Check for captures first (mandatory capture rule)
        for dr, dc in directions:
            # Check if adjacent square has opponent's piece
            r, c = row + dr, col + dc
            if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                if (piece in (1, 3) and board[r][c] in (2, 4)) or \
                   (piece in (2, 4) and board[r][c] in (1, 3)):
                    # Check if landing square is empty
                    r2, c2 = r + dr, c + dc
                    if 0 <= r2 < self.BOARD_SIZE and 0 <= c2 < self.BOARD_SIZE and board[r2][c2] == 0:
                        captures.append((r2, c2))
        
        if captures:
            return captures
        
        # If no captures, check for regular moves
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and board[r][c] == 0:
                moves.append((r, c))
        
        return moves
    
    def evaluate_board(self, board):
        """Evaluate the board state from the AI's perspective."""
        ai_score = 0
        player_score = 0
        
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = board[row][col]
                if piece == 1:  # Player piece
                    player_score += 1
                    # Encourage advancing pieces
                    player_score += (self.BOARD_SIZE - 1 - row) * 0.1
                elif piece == 2:  # AI piece
                    ai_score += 1
                    # Encourage advancing pieces
                    ai_score += row * 0.1
                elif piece == 3:  # Player king
                    player_score += 1.5
                elif piece == 4:  # AI king
                    ai_score += 1.5
        
        # Encourage controlling the center
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        for row, col in center_squares:
            piece = board[row][col]
            if piece == 1 or piece == 3:
                player_score += 0.2
            elif piece == 2 or piece == 4:
                ai_score += 0.2
        
        return ai_score - player_score
    
    def check_game_over(self):
        """Check if the game is over (no pieces left or no valid moves)."""
        player_has_pieces = False
        ai_has_pieces = False
        
        # Check if either player has no pieces left
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] in (1, 3):
                    player_has_pieces = True
                elif self.board[row][col] in (2, 4):
                    ai_has_pieces = True
        
        if not player_has_pieces:
            self.game_over = True
            messagebox.showinfo("Game Over", f"AI wins! {self.player_name} has no pieces left.")
            return
        if not ai_has_pieces:
            self.game_over = True
            messagebox.showinfo("Game Over", f"{self.player_name} wins! AI has no pieces left.")
            return
        
        # Check if current player has any valid moves
        if self.current_player == "player":
            has_valid_move = False
            for row in range(self.BOARD_SIZE):
                for col in range(self.BOARD_SIZE):
                    if self.board[row][col] in (1, 3):
                        if self.get_valid_moves(row, col):
                            has_valid_move = True
                            break
                if has_valid_move:
                    break
            
            if not has_valid_move:
                self.game_over = True
                messagebox.showinfo("Game Over", f"AI wins! {self.player_name} has no valid moves.")
        
        elif self.current_player == "ai":
            has_valid_move = False
            for row in range(self.BOARD_SIZE):
                for col in range(self.BOARD_SIZE):
                    if self.board[row][col] in (2, 4):
                        if self.get_valid_moves(row, col):
                            has_valid_move = True
                            break
                if has_valid_move:
                    break
            
            if not has_valid_move:
                self.game_over = True
                messagebox.showinfo("Game Over", f"{self.player_name} wins! AI has no valid moves.")
    
    def update_status(self):
        """Update the status label."""
        if self.game_over:
            self.status_label.config(text="Game Over!")
        elif self.current_player == "player":
            self.status_label.config(text=f"{self.player_name}'s turn (Black)", fg="black")
        else:
            self.status_label.config(text="AI's turn (White)", fg="gray")

# Create and run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = CheckersGame(root)
    root.mainloop()