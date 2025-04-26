import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import random
from copy import deepcopy
import time

class CheckersGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced Checkers Game with AI")
        self.master.geometry("800x800")
        self.master.minsize(600, 700)
        
        # Game settings
        self.player_name = ""
        self.ai_difficulty = 3  # Default medium
        self.ai_algorithm = "minimax"  # Default algorithm
        
        # Theme settings
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_theme()
        
        # Show start screen
        self.show_start_screen()
    
    def configure_theme(self):
        """Configure custom theme for modern look."""
        self.style.configure('TFrame', background='#f5f5f5')
        self.style.configure('TLabel', background='#f5f5f5', font=('Helvetica', 12))
        self.style.configure('TButton', padding=10, font=('Helvetica', 11))
        self.style.configure('TRadiobutton', background='#f5f5f5', font=('Helvetica', 10))
        self.style.map('TButton', 
                       background=[('active', '#45a049')],
                       foreground=[('active', 'white')])
    
    def show_start_screen(self):
        """Show enhanced start screen with name, difficulty, and algorithm selection."""
        self.start_frame = ttk.Frame(self.master, padding=20)
        self.start_frame.pack(expand=True, fill=tk.BOTH)
        
        # Title
        title_label = ttk.Label(
            self.start_frame, 
            text="Checkers: Ultimate Edition", 
            font=("Helvetica", 28, "bold"),
            foreground="#2e7d32"
        )
        title_label.pack(pady=30)
        
        # Input frame
        input_frame = ttk.Frame(self.start_frame)
        input_frame.pack(pady=10)
        
        # Name entry
        name_frame = ttk.Frame(input_frame)
        name_frame.pack(pady=10, fill=tk.X)
        ttk.Label(name_frame, text="Player Name:").pack(side=tk.LEFT)
        self.name_entry = ttk.Entry(name_frame, font=("Helvetica", 12), width=20)
        self.name_entry.pack(side=tk.LEFT, padx=10)
        self.name_entry.focus()
        
        # Difficulty selection
        diff_frame = ttk.Frame(input_frame)
        diff_frame.pack(pady=10, fill=tk.X)
        ttk.Label(diff_frame, text="AI Difficulty:").pack(side=tk.LEFT)
        self.difficulty = tk.StringVar(value="medium")
        difficulties = [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]
        for text, mode in difficulties:
            rb = ttk.Radiobutton(
                diff_frame, 
                text=text, 
                variable=self.difficulty,
                value=mode
            )
            rb.pack(side=tk.LEFT, padx=10)
        
        # Algorithm selection
        algo_frame = ttk.Frame(input_frame)
        algo_frame.pack(pady=10, fill=tk.X)
        ttk.Label(algo_frame, text="AI Algorithm:").pack(side=tk.LEFT)
        self.algorithm = tk.StringVar(value="minimax")
        algorithms = [
            ("Minimax", "minimax"),
            ("Negamax", "negamax"),
            ("Monte Carlo TS", "mcts")
        ]
        for text, algo in algorithms:
            rb = ttk.Radiobutton(
                algo_frame, 
                text=text, 
                variable=self.algorithm,
                value=algo
            )
            rb.pack(side=tk.LEFT, padx=10)
        
        # Start button
        start_button = ttk.Button(
            self.start_frame,
            text="Start Game",
            command=self.start_game,
            style='Accent.TButton'
        )
        self.style.configure('Accent.TButton', background='#4CAF50', foreground='white')
        start_button.pack(pady=30)
        
        # Instructions
        ttk.Label(
            self.start_frame,
            text="Select your name, difficulty, and AI algorithm to begin!",
            font=("Helvetica", 10, "italic"),
            foreground="gray"
        ).pack(pady=10)
    
    def start_game(self):
        """Start the game with selected settings."""
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            messagebox.showwarning("Input Error", "Please enter your name")
            return
        
        # Set AI difficulty
        difficulty_map = {"easy": 2, "medium": 3, "hard": 5}
        self.ai_difficulty = difficulty_map[self.difficulty.get()]
        
        # Set AI algorithm
        self.ai_algorithm = self.algorithm.get()
        
        # Remove start screen
        self.start_frame.destroy()
        
        # Initialize game
        self.init_game()
    
    def init_game(self):
        """Initialize the game."""
        # Game constants
        self.BOARD_SIZE = 8
        self.PADDING = 20
        self.CIRCLE_PADDING = 10
        
        # Colors
        self.BOARD_COLOR1 = "#e0c9a6"
        self.BOARD_COLOR2 = "#5c4033"
        self.HIGHLIGHT_COLOR = "#81c784"
        self.PLAYER_COLOR = "#212121"
        self.AI_COLOR = "#f5f5f5"
        self.KING_COLOR = "#ffd700"
        self.VALID_MOVE_COLOR = "#a5d6a7"
        self.BG_COLOR = "#f5f5f5"
        
        # Game state
        self.board = self.create_initial_board()
        self.current_player = "player"
        self.selected_piece = None
        self.valid_moves = []
        self.game_over = False
        self.move_history = []
        
        # AI settings
        self.ai_depth = self.ai_difficulty
        
        # Create GUI
        self.create_widgets()
        self.draw_board()
        self.update_status()
    
    def create_widgets(self):
        """Create enhanced GUI widgets."""
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top frame for status and controls
        self.top_frame = ttk.Frame(self.main_frame)
        self.top_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Status label
        self.status_label = ttk.Label(
            self.top_frame,
            text="",
            font=("Helvetica", 14, "bold")
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Settings button
        settings_button = ttk.Button(
            self.top_frame,
            text="⚙ Settings",
            command=self.show_settings,
            style='TButton'
        )
        settings_button.pack(side=tk.RIGHT, padx=5)
        
        # Move history
        history_button = ttk.Button(
            self.top_frame,
            text="📜 History",
            command=self.show_move_history,
            style='TButton'
        )
        history_button.pack(side=tk.RIGHT, padx=5)
        
        # Canvas container
        self.canvas_container = ttk.Frame(self.main_frame)
        self.canvas_container.pack(fill=tk.BOTH, expand=True)
        self.canvas_container.grid_rowconfigure(0, weight=1)
        self.canvas_container.grid_columnconfigure(0, weight=1)
        
        # Canvas
        self.canvas = tk.Canvas(
            self.canvas_container, 
            bg=self.BG_COLOR,
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Bind events
        self.canvas.bind("<Button-1>", self.on_square_clicked)
        self.master.bind("<Configure>", self.on_window_resize)
        
        # Update board size
        self.update_board_size()
    
    def show_settings(self):
        """Show settings window to change difficulty or algorithm."""
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.geometry("300x300")
        settings_window.transient(self.master)
        settings_window.grab_set()
        
        frame = ttk.Frame(settings_window, padding=20)
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Difficulty
        ttk.Label(frame, text="AI Difficulty:").pack(anchor=tk.W)
        diff_var = tk.StringVar(value=self.difficulty.get())
        for text, mode in [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]:
            ttk.Radiobutton(
                frame, 
                text=text, 
                variable=diff_var, 
                value=mode
            ).pack(anchor=tk.W)
        
        # Algorithm
        ttk.Label(frame, text="AI Algorithm:").pack(anchor=tk.W, pady=(10, 0))
        algo_var = tk.StringVar(value=self.ai_algorithm)
        for text, algo in [("Minimax", "minimax"), ("Negamax", "negamax"), ("Monte Carlo TS", "mcts")]:
            ttk.Radiobutton(
                frame, 
                text=text, 
                variable=algo_var, 
                value=algo
            ).pack(anchor=tk.W)
        
        # Apply button
        def apply_settings():
            difficulty_map = {"easy": 2, "medium": 3, "hard": 5}
            self.ai_difficulty = difficulty_map[diff_var.get()]
            self.ai_algorithm = algo_var.get()
            self.ai_depth = self.ai_difficulty
            settings_window.destroy()
            self.update_status()
        
        ttk.Button(
            frame,
            text="Apply",
            command=apply_settings,
            style='Accent.TButton'
        ).pack(pady=20)
    
    def show_move_history(self):
        """Show move history in a new window."""
        history_window = tk.Toplevel(self.master)
        history_window.title("Move History")
        history_window.geometry("400x400")
        history_window.transient(self.master)
        history_window.grab_set()
        
        frame = ttk.Frame(history_window, padding=10)
        frame.pack(expand=True, fill=tk.BOTH)
        
        text_area = tk.Text(frame, height=20, width=40, font=("Helvetica", 10))
        text_area.pack(pady=10)
        
        for i, move in enumerate(self.move_history):
            player = move['player']
            from_pos = move['from']
            to_pos = move['to']
            text_area.insert(tk.END, f"Move {i+1}: {player} from {from_pos} to {to_pos}\n")
        
        text_area.config(state='disabled')
        
        ttk.Button(
            frame,
            text="Close",
            command=history_window.destroy
        ).pack(pady=10)
    
    def update_board_size(self, event=None):
        """Update board size responsively."""
        container_width = self.canvas_container.winfo_width()
        container_height = self.canvas_container.winfo_height()
        max_square_width = (container_width - 2 * self.PADDING) // self.BOARD_SIZE
        max_square_height = (container_height - 2 * self.PADDING) // self.BOARD_SIZE
        self.SQUARE_SIZE = min(max_square_width, max_square_height, 100)
        self.SQUARE_SIZE = max(10, self.SQUARE_SIZE)
        board_width = self.BOARD_SIZE * self.SQUARE_SIZE + 2 * self.PADDING
        board_height = self.BOARD_SIZE * self.SQUARE_SIZE + 2 * self.PADDING
        self.canvas.config(width=board_width, height=board_height)
        self.draw_board()
    
    def on_window_resize(self, event):
        """Handle window resize."""
        if hasattr(self, 'canvas_container'):
            self.update_board_size()
    
    def create_initial_board(self):
        """Create initial board setup."""
        board = np.zeros((self.BOARD_SIZE, self.BOARD_SIZE), dtype=int)
        for row in range(3):
            for col in range(self.BOARD_SIZE):
                if (row + col) % 2 == 1:
                    board[row][col] = 1  # Player pieces
        for row in range(5, 8):
            for col in range(self.BOARD_SIZE):
                if (row + col) % 2 == 1:
                    board[row][col] = 2  # AI pieces
        return board
    
    def draw_board(self):
        """Draw the checkerboard with enhanced visuals."""
        self.canvas.delete("all")
        
        # Draw squares with shadow effect
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                x1 = self.PADDING + col * self.SQUARE_SIZE
                y1 = self.PADDING + row * self.SQUARE_SIZE
                x2 = x1 + self.SQUARE_SIZE
                y2 = y1 + self.SQUARE_SIZE
                color = self.BOARD_COLOR1 if (row + col) % 2 == 0 else self.BOARD_COLOR2
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#333333", width=1)
                
                # Highlight selected piece
                if self.selected_piece and self.selected_piece == (row, col):
                    self.canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2, 
                        fill="", 
                        outline=self.HIGHLIGHT_COLOR,
                        width=3
                    )
                
                # Highlight valid moves
                if (row, col) in self.valid_moves:
                    self.canvas.create_oval(
                        x1 + self.SQUARE_SIZE//3, y1 + self.SQUARE_SIZE//3,
                        x2 - self.SQUARE_SIZE//3, y2 - self.SQUARE_SIZE//3,
                        fill=self.VALID_MOVE_COLOR, 
                        outline="",
                        stipple="gray50"
                    )
        
        # Draw pieces with gradient
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = self.board[row][col]
                if piece != 0:
                    self.draw_piece(row, col, piece)
    
    def draw_piece(self, row, col, piece):
        """Draw a piece with enhanced visuals."""
        x1 = self.PADDING + col * self.SQUARE_SIZE + self.CIRCLE_PADDING
        y1 = self.PADDING + row * self.SQUARE_SIZE + self.CIRCLE_PADDING
        x2 = x1 + (self.SQUARE_SIZE - 2 * self.CIRCLE_PADDING)
        y2 = y1 + (self.SQUARE_SIZE - 2 * self.CIRCLE_PADDING)
        
        if piece == 1:
            color = self.PLAYER_COLOR
            king = False
        elif piece == 2:
            color = self.AI_COLOR
            king = False
        elif piece == 3:
            color = self.PLAYER_COLOR
            king = True
        elif piece == 4:
            color = self.AI_COLOR
            king = True
        
        # Gradient effect
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="#333333", width=2)
        self.canvas.create_oval(
            x1 + 2, y1 + 2, x2 - 2, y2 - 2,
            fill="", outline="#ffffff", width=1, stipple="gray25"
        )
        
        if king:
            crown_x = (x1 + x2) / 2
            crown_y = (y1 + y2) / 2
            self.canvas.create_text(
                crown_x, crown_y, 
                text="♛", 
                fill=self.KING_COLOR, 
                font=("Helvetica", max(12, int(self.SQUARE_SIZE/4)))
            )
    
    def on_square_clicked(self, event):
        """Handle board clicks."""
        if self.game_over or self.current_player != "player":
            return
        
        col = (event.x - self.PADDING) // self.SQUARE_SIZE
        row = (event.y - self.PADDING) // self.SQUARE_SIZE
        
        if not (0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE):
            return
        
        if self.selected_piece is None:
            piece = self.board[row][col]
            if piece in (1, 3):
                self.selected_piece = (row, col)
                self.valid_moves = self.get_valid_moves(row, col)
                self.draw_board()
        else:
            selected_row, selected_col = self.selected_piece
            if (row, col) in self.valid_moves:
                self.make_move(selected_row, selected_col, row, col)
                self.move_history.append({
                    'player': self.player_name,
                    'from': (selected_row, selected_col),
                    'to': (row, col)
                })
                self.selected_piece = None
                self.valid_moves = []
                self.draw_board()
                if not self.game_over and self.current_player == "ai":
                    self.master.after(500, self.ai_move)
            else:
                piece = self.board[row][col]
                if piece in (1, 3):
                    self.selected_piece = (row, col)
                    self.valid_moves = self.get_valid_moves(row, col)
                    self.draw_board()
    
    def get_valid_moves(self, row, col):
        """Get valid moves for a piece."""
        piece = self.board[row][col]
        moves = []
        captures = []
        
        if piece == 1:
            directions = [(1, -1), (1, 1)]
        elif piece == 2:
            directions = [(-1, -1), (-1, 1)]
        elif piece in (3, 4):
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                if (piece in (1, 3) and self.board[r][c] in (2, 4)) or \
                   (piece in (2, 4) and self.board[r][c] in (1, 3)):
                    r2, c2 = r + dr, c + dc
                    if 0 <= r2 < self.BOARD_SIZE and 0 <= c2 < self.BOARD_SIZE and self.board[r2][c2] == 0:
                        captures.append((r2, c2))
        
        if captures:
            return captures
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and self.board[r][c] == 0:
                moves.append((r, c))
        
        return moves
    
    def make_move(self, from_row, from_col, to_row, to_col):
        """Execute a move."""
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
                self.draw_board()
                return
        
        if piece == 1 and to_row == self.BOARD_SIZE - 1:
            self.board[to_row][to_col] = 3
        elif piece == 2 and to_row == 0:
            self.board[to_row][to_col] = 4
        
        self.current_player = "ai" if self.current_player == "player" else "player"
        self.check_game_over()
        self.update_status()
    
    def ai_move(self):
        """Execute AI move based on selected algorithm."""
        if self.game_over or self.current_player != "ai":
            return
        
        start_time = time.time()
        
        if self.ai_algorithm == "minimax":
            move = self.minimax_move()
        elif self.ai_algorithm == "negamax":
            move = self.negamax_move()
        else:  # mcts
            move = self.mcts_move()
        
        if move:
            from_row, from_col, to_row, to_col = move
            self.move_history.append({
                'player': 'AI',
                'from': (from_row, from_col),
                'to': (to_row, to_col)
            })
            self.make_move(from_row, from_col, to_row, to_col)
            self.draw_board()
        else:
            self.current_player = "player"
            self.update_status()
        
        print(f"AI move time: {time.time() - start_time:.2f}s")
    
    def minimax_move(self):
        """Minimax algorithm for AI move."""
        best_score = -float('inf')
        best_move = None
        ai_pieces = [(r, c) for r in range(self.BOARD_SIZE) for c in range(self.BOARD_SIZE) if self.board[r][c] in (2, 4)]
        
        for row, col in ai_pieces:
            moves = self.get_valid_moves(row, col)
            for move_row, move_col in moves:
                temp_board = deepcopy(self.board)
                temp_board[row][col] = 0
                temp_board[move_row][move_col] = self.board[row][col]
                if abs(row - move_row) == 2:
                    captured_row = (row + move_row) // 2
                    captured_col = (col + move_col) // 2
                    temp_board[captured_row][captured_col] = 0
                if temp_board[move_row][move_col] == 2 and move_row == 0:
                    temp_board[move_row][move_col] = 4
                score = self.minimax(temp_board, self.ai_depth - 1, -float('inf'), float('inf'), False)
                if score > best_score:
                    best_score = score
                    best_move = (row, col, move_row, move_col)
        
        return best_move
    
    def minimax(self, board, depth, alpha, beta, maximizing_player):
        """Minimax with alpha-beta pruning."""
        if depth == 0 or self.is_terminal(board):
            return self.evaluate_board(board)
        
        if maximizing_player:
            max_eval = -float('inf')
            for row, col in [(r, c) for r in range(self.BOARD_SIZE) for c in range(self.BOARD_SIZE) if board[r][c] in (2, 4)]:
                moves = self.get_valid_moves_for_board(board, row, col)
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
                    eval_score = self.minimax(temp_board, depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval_score)
                    alpha = max(alpha, eval_score)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for row, col in [(r, c) for r in range(self.BOARD_SIZE) for c in range(self.BOARD_SIZE) if board[r][c] in (1, 3)]:
                moves = self.get_valid_moves_for_board(board, row, col)
                for move_row, move_col in moves:
                    temp_board = deepcopy(board)
                    temp_board[row][col] = 0
                    temp_board[move_row][move_col] = board[row][col]
                    if abs(row - move_row) == 2:
                        captured_row = (row + move_row) // 2
                        captured_col = (col + move_col) // 2
                        temp_board[captured_row][captured_col] = 0
                    if temp_board[move_row][move_col] == 1 and move_row == self.BOARD_SIZE - 1:
                        temp_board[move_row][move_col] = 3
                    eval_score = self.minimax(temp_board, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval_score)
                    beta = min(beta, eval_score)
                    if beta <= alpha:
                        break
            return min_eval
    
    def negamax_move(self):
        """Negamax algorithm for AI move."""
        best_score = -float('inf')
        best_move = None
        ai_pieces = [(r, c) for r in range(self.BOARD_SIZE) for c in range(self.BOARD_SIZE) if self.board[r][c] in (2, 4)]
        
        for row, col in ai_pieces:
            moves = self.get_valid_moves(row, col)
            for move_row, move_col in moves:
                temp_board = deepcopy(self.board)
                temp_board[row][col] = 0
                temp_board[move_row][move_col] = self.board[row][col]
                if abs(row - move_row) == 2:
                    captured_row = (row + move_row) // 2
                    captured_col = (col + move_col) // 2
                    temp_board[captured_row][captured_col] = 0
                if temp_board[move_row][move_col] == 2 and move_row == 0:
                    temp_board[move_row][move_col] = 4
                score = -self.negamax(temp_board, self.ai_depth - 1, -float('inf'), float('inf'), -1)
                if score > best_score:
                    best_score = score
                    best_move = (row, col, move_row, move_col)
        
        return best_move
    
    def negamax(self, board, depth, alpha, beta, color):
        """Negamax with alpha-beta pruning."""
        if depth == 0 or self.is_terminal(board):
            return color * self.evaluate_board(board)
        
        max_score = -float('inf')
        piece_types = (2, 4) if color == 1 else (1, 3)
        pieces = [(r, c) for r in range(self.BOARD_SIZE) for c in range(self.BOARD_SIZE) if board[r][c] in piece_types]
        
        for row, col in pieces:
            moves = self.get_valid_moves_for_board(board, row, col)
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
                elif temp_board[move_row][move_col] == 1 and move_row == self.BOARD_SIZE - 1:
                    temp_board[move_row][move_col] = 3
                score = -self.negamax(temp_board, depth - 1, -beta, -alpha, -color)
                max_score = max(max_score, score)
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
        return max_score
    
    def mcts_move(self):
        """Monte Carlo Tree Search for AI move."""
        root = MCTSNode(self.board, None, None, self)
        iterations = 800 if self.ai_difficulty >= 3 else 400
        
        for _ in range(iterations):
            node = root
            while node.children and not node.is_terminal():
                node = node.select_child()
            if not node.is_terminal():
                node.expand()
                if node.children:
                    node = random.choice(node.children)
            reward = node.simulate()
            node.backpropagate(reward)
        
        best_child = max(root.children, key=lambda c: c.visits) if root.children else None
        if best_child and best_child.move:
            return best_child.move
        return None
    
    def get_valid_moves_for_board(self, board, row, col):
        """Get valid moves for a piece on a given board."""
        piece = board[row][col]
        moves = []
        captures = []
        
        if piece == 1:
            directions = [(1, -1), (1, 1)]
        elif piece == 2:
            directions = [(-1, -1), (-1, 1)]
        elif piece in (3, 4):
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            r = row + dr
            c = col + dc
            if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE:
                if (piece in (1, 3) and board[r][c] in (2, 4)) or \
                   (piece in (2, 4) and board[r][c] in (1, 3)):
                    r2 = r + dr
                    c2 = c + dc
                    if 0 <= r2 < self.BOARD_SIZE and 0 <= c2 < self.BOARD_SIZE and board[r2][c2] == 0:
                        captures.append((r2, c2))
        
        if captures:
            return captures
        
        for dr, dc in directions:
            r = row + dr
            c = col + dc
            if 0 <= r < self.BOARD_SIZE and 0 <= c < self.BOARD_SIZE and board[r][c] == 0:
                moves.append((r, c))
        
        return moves
    
    def evaluate_board(self, board):
        """Evaluate board from AI's perspective."""
        ai_score = 0
        player_score = 0
        
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                piece = board[row][col]
                if piece == 1:
                    player_score += 1
                    player_score += (self.BOARD_SIZE - 1 - row) * 0.1
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
    
    def is_terminal(self, board):
        """Check if board state is terminal."""
        player_pieces = any(board[r][c] in (1, 3) for r in range(self.BOARD_SIZE) for c in range(self.BOARD_SIZE))
        ai_pieces = any(board[r][c] in (2, 4) for r in range(self.BOARD_SIZE) for c in range(self.BOARD_SIZE))
        if not player_pieces or not ai_pieces:
            return True
        
        ai_moves = any(self.get_valid_moves_for_board(board, r, c) 
                       for r in range(self.BOARD_SIZE) for c in range(self.BOARD_SIZE) if board[r][c] in (2, 4))
        player_moves = any(self.get_valid_moves_for_board(board, r, c) 
                           for r in range(self.BOARD_SIZE) for c in range(self.BOARD_SIZE) if board[r][c] in (1, 3))
        return not ai_moves or not player_moves
    
    def check_game_over(self):
        """Check for game over conditions."""
        player_has_pieces = False
        ai_has_pieces = False
        
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
        
        if self.current_player == "player":
            has_valid_move = any(self.get_valid_moves(r, c) 
                                for r in range(self.BOARD_SIZE) for c in range(self.BOARD_SIZE) if self.board[r][c] in (1, 3))
            if not has_valid_move:
                self.game_over = True
                messagebox.showinfo("Game Over", f"AI wins! {self.player_name} has no valid moves.")
        
        elif self.current_player == "ai":
            has_valid_move = any(self.get_valid_moves(r, c) 
                                for r in range(self.BOARD_SIZE) for c in range(self.BOARD_SIZE) if self.board[r][c] in (2, 4))
            if not has_valid_move:
                self.game_over = True
                messagebox.showinfo("Game Over", f"{self.player_name} wins! AI has no valid moves.")
    
    def update_status(self):
        """Update status label."""
        if self.game_over:
            self.status_label.config(text="Game Over!")
        elif self.current_player == "player":
            self.status_label.config(text=f"{self.player_name}'s turn (Black) | {self.ai_algorithm.capitalize()}", foreground="#212121")
        else:
            self.status_label.config(text=f"AI's turn (White) | {self.ai_algorithm.capitalize()}", foreground="#555555")

class MCTSNode:
    def __init__(self, board, move, parent, game):
        self.board = deepcopy(board)
        self.move = move
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.game = game
    
    def is_terminal(self):
        return self.game.is_terminal(self.board)
    
    def expand(self):
        pieces = [(r, c) for r in range(self.game.BOARD_SIZE) for c in range(self.game.BOARD_SIZE) if self.board[r][c] in (2, 4)]
        for row, col in pieces:
            moves = self.game.get_valid_moves_for_board(self.board, row, col)
            for move_row, move_col in moves:
                new_board = deepcopy(self.board)
                new_board[row][col] = 0
                new_board[move_row][move_col] = self.board[row][col]
                if abs(row - move_row) == 2:
                    captured_row = (row + move_row) // 2
                    captured_col = (col + move_col) // 2
                    new_board[captured_row][captured_col] = 0
                if new_board[move_row][move_col] == 2 and move_row == 0:
                    new_board[move_row][move_col] = 4
                self.children.append(MCTSNode(new_board, (row, col, move_row, move_col), self, self.game))
    
    def simulate(self):
        current_board = deepcopy(self.board)
        current_player = 'ai'
        max_steps = 50
        
        for _ in range(max_steps):
            if self.game.is_terminal(current_board):
                score = self.game.evaluate_board(current_board)
                return 1 if score > 0 else -1 if score < 0 else 0
            
            piece_types = (2, 4) if current_player == 'ai' else (1, 3)
            pieces = [(r, c) for r in range(self.game.BOARD_SIZE) for c in range(self.game.BOARD_SIZE) 
                      if current_board[r][c] in piece_types]
            if not pieces:
                return -1 if current_player == 'ai' else 1
            
            row, col = random.choice(pieces)
            moves = self.game.get_valid_moves_for_board(current_board, row, col)
            if not moves:
                return -1 if current_player == 'ai' else 1
            
            move_row, move_col = random.choice(moves)
            current_board[row][col] = 0
            current_board[move_row][move_col] = current_board[row][col]
            if abs(row - move_row) == 2:
                captured_row = (row + move_row) // 2
                captured_col = (col + move_col) // 2
                current_board[captured_row][captured_col] = 0
            if current_board[move_row][move_col] == 2 and move_row == 0:
                current_board[move_row][move_col] = 4
            elif current_board[move_row][move_col] == 1 and move_row == self.game.BOARD_SIZE - 1:
                current_board[move_row][move_col] = 3
            current_player = 'player' if current_player == 'ai' else 'ai'
        
        return self.game.evaluate_board(current_board) / 10
    
    def backpropagate(self, reward):
        self.visits += 1
        self.wins += reward
        if self.parent:
            self.parent.backpropagate(-reward)
    
    def select_child(self):
        exploration = 1.414
        return max(self.children, key=lambda c: (c.wins / c.visits if c.visits > 0 else 0) + 
                   exploration * (2 * np.log(self.visits) / c.visits)**0.5 if c.visits > 0 else float('inf'))

if __name__ == "__main__":
    root = tk.Tk()
    game = CheckersGame(root)
    root.mainloop()