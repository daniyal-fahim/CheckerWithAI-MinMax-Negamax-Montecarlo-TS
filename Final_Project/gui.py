import tkinter as tk
from tkinter import messagebox, ttk
from game_logic import CheckersLogic
from utils import Constants

class CheckersGUI:
    """Handles the graphical user interface for the Checkers game."""
    
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced Checkers Game with AI")
        self.master.geometry("800x800")
        self.master.minsize(600, 700)
        
        self.player_name = ""
        self.difficulty = tk.StringVar(value="medium")
        self.algorithm = tk.StringVar(value="minimax")
        self.style = ttk.Style()
        self.configure_theme()
        
        self.game_logic = None
        self.show_start_screen()
    
    def configure_theme(self):
        """Configure custom theme for modern look."""
        self.style.theme_use('clam')
        self.style.configure('TFrame', background=Constants.BG_COLOR)
        self.style.configure('TLabel', background=Constants.BG_COLOR, font=('Helvetica', 12))
        self.style.configure('TButton', padding=10, font=('Helvetica', 11))
        self.style.configure('TRadiobutton', background=Constants.BG_COLOR, font=('Helvetica', 10))
        self.style.configure('Accent.TButton', background='#4CAF50', foreground='white')
        self.style.map('TButton', background=[('active', '#45a049')], foreground=[('active', 'white')])
    
    def show_start_screen(self):
        """Display the start screen with name, difficulty, and algorithm selection."""
        self.start_frame = ttk.Frame(self.master, padding=20)
        self.start_frame.pack(expand=True, fill=tk.BOTH)
        
        ttk.Label(
            self.start_frame,
            text="Checkers: Ultimate Edition",
            font=("Helvetica", 28, "bold"),
            foreground="#2e7d32"
        ).pack(pady=30)
        
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
        for text, mode in [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]:
            ttk.Radiobutton(diff_frame, text=text, variable=self.difficulty, value=mode).pack(side=tk.LEFT, padx=10)
        
        # Algorithm selection
        algo_frame = ttk.Frame(input_frame)
        algo_frame.pack(pady=10, fill=tk.X)
        ttk.Label(algo_frame, text="AI Algorithm:").pack(side=tk.LEFT)
        algorithms = [("Minimax", "minimax"), ("Negamax", "negamax"), ("Monte Carlo TS", "mcts")]
        for text, algo in algorithms:
            ttk.Radiobutton(algo_frame, text=text, variable=self.algorithm, value=algo).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            self.start_frame,
            text="Start Game",
            command=self.start_game,
            style='Accent.TButton'
        ).pack(pady=30)
        
        ttk.Label(
            self.start_frame,
            text="Select your name, difficulty, and AI algorithm to begin!",
            font=("Helvetica", 10, "italic"),
            foreground="gray"
        ).pack(pady=10)
    
    def start_game(self):
        """Initialize the game with selected settings."""
        self.player_name = self.name_entry.get().strip()
        if not self.player_name:
            messagebox.showwarning("Input Error", "Please enter your name")
            return
        
        difficulty_map = {"easy": 2, "medium": 3, "hard": 5}
        ai_difficulty = difficulty_map[self.difficulty.get()]
        ai_algorithm = self.algorithm.get()
        
        self.start_frame.destroy()
        self.game_logic = CheckersLogic(ai_difficulty, ai_algorithm)
        self.setup_game_gui()
    
    def setup_game_gui(self):
        """Set up the main game GUI."""
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.top_frame = ttk.Frame(self.main_frame)
        self.top_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(self.top_frame, text="", font=("Helvetica", 14, "bold"))
        self.status_label.pack(side=tk.LEFT)
        
        ttk.Button(self.top_frame, text="⚙ Settings", command=self.show_settings, style='TButton').pack(side=tk.RIGHT, padx=5)
        ttk.Button(self.top_frame, text="📜 History", command=self.show_move_history, style='TButton').pack(side=tk.RIGHT, padx=5)
        
        self.canvas_container = ttk.Frame(self.main_frame)
        self.canvas_container.pack(fill=tk.BOTH, expand=True)
        self.canvas_container.grid_rowconfigure(0, weight=1)
        self.canvas_container.grid_columnconfigure(0, weight=1)
        
        self.canvas = tk.Canvas(self.canvas_container, bg=Constants.BG_COLOR, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        self.canvas.bind("<Button-1>", self.on_square_clicked)
        self.master.bind("<Configure>", self.on_window_resize)
        self.update_board_size()
        self.update_status()
    
    def show_settings(self):
        """Show settings window to change difficulty or algorithm."""
        settings_window = tk.Toplevel(self.master)
        settings_window.title("Settings")
        settings_window.geometry("300x300")
        settings_window.transient(self.master)
        settings_window.grab_set()
        
        frame = ttk.Frame(settings_window, padding=20)
        frame.pack(expand=True, fill=tk.BOTH)
        
        ttk.Label(frame, text="AI Difficulty:").pack(anchor=tk.W)
        diff_var = tk.StringVar(value=self.difficulty.get())
        for text, mode in [("Easy", "easy"), ("Medium", "medium"), ("Hard", "hard")]:
            ttk.Radiobutton(frame, text=text, variable=diff_var, value=mode).pack(anchor=tk.W)
        
        ttk.Label(frame, text="AI Algorithm:").pack(anchor=tk.W, pady=(10, 0))
        algo_var = tk.StringVar(value=self.algorithm.get())
        algorithms = [("Minimax", "minimax"), ("Negamax", "negamax"), ("Monte Carlo TS", "mcts")]
        for text, algo in algorithms:
            ttk.Radiobutton(frame, text=text, variable=algo_var, value=algo).pack(anchor=tk.W)
        
        def apply_settings():
            difficulty_map = {"easy": 2, "medium": 3, "hard": 5}
            self.game_logic.ai_difficulty = difficulty_map[diff_var.get()]
            self.game_logic.ai_algorithm = algo_var.get()
            settings_window.destroy()
            self.update_status()
        
        ttk.Button(frame, text="Apply", command=apply_settings, style='Accent.TButton').pack(pady=20)
    
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
        
        for i, move in enumerate(self.game_logic.move_history):
            player = move['player']
            from_pos = move['from']
            to_pos = move['to']
            text_area.insert(tk.END, f"Move {i+1}: {player} from {from_pos} to {to_pos}\n")
        
        text_area.config(state='disabled')
        ttk.Button(frame, text="Close", command=history_window.destroy).pack(pady=10)
    
    def update_board_size(self, event=None):
        """Update board size responsively."""
        container_width = self.canvas_container.winfo_width()
        container_height = self.canvas_container.winfo_height()
        max_square_width = (container_width - 2 * Constants.PADDING) // self.game_logic.board_size
        max_square_height = (container_height - 2 * Constants.PADDING) // self.game_logic.board_size
        self.game_logic.square_size = min(max_square_width, max_square_height, 100)
        self.game_logic.square_size = max(10, self.game_logic.square_size)
        board_width = self.game_logic.board_size * self.game_logic.square_size + 2 * Constants.PADDING
        board_height = self.game_logic.board_size * self.game_logic.square_size + 2 * Constants.PADDING
        self.canvas.config(width=board_width, height=board_height)
        self.draw_board()
    
    def on_window_resize(self, event):
        """Handle window resize."""
        if hasattr(self, 'canvas_container'):
            self.update_board_size()
    
    def draw_board(self):
        """Draw the checkerboard with enhanced visuals."""
        self.canvas.delete("all")
        
        for row in range(self.game_logic.board_size):
            for col in range(self.game_logic.board_size):
                x1 = Constants.PADDING + col * self.game_logic.square_size
                y1 = Constants.PADDING + row * self.game_logic.square_size
                x2 = x1 + self.game_logic.square_size
                y2 = y1 + self.game_logic.square_size
                color = Constants.BOARD_COLOR1 if (row + col) % 2 == 0 else Constants.BOARD_COLOR2
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#333333", width=1)
                
                if self.game_logic.selected_piece == (row, col):
                    self.canvas.create_rectangle(
                        x1 + 2, y1 + 2, x2 - 2, y2 - 2,
                        fill="", outline=Constants.HIGHLIGHT_COLOR, width=3
                    )
                
                if (row, col) in self.game_logic.valid_moves:
                    self.canvas.create_oval(
                        x1 + self.game_logic.square_size//3, y1 + self.game_logic.square_size//3,
                        x2 - self.game_logic.square_size//3, y2 - self.game_logic.square_size//3,
                        fill=Constants.VALID_MOVE_COLOR, outline="", stipple="gray50"
                    )
        
        for row in range(self.game_logic.board_size):
            for col in range(self.game_logic.board_size):
                piece = self.game_logic.board[row][col]
                if piece != 0:
                    self.draw_piece(row, col, piece)
    
    def draw_piece(self, row, col, piece):
        """Draw a piece with enhanced visuals."""
        x1 = Constants.PADDING + col * self.game_logic.square_size + Constants.CIRCLE_PADDING
        y1 = Constants.PADDING + row * self.game_logic.square_size + Constants.CIRCLE_PADDING
        x2 = x1 + (self.game_logic.square_size - 2 * Constants.CIRCLE_PADDING)
        y2 = y1 + (self.game_logic.square_size - 2 * Constants.CIRCLE_PADDING)
        
        if piece == 1:
            color = Constants.PLAYER_COLOR
            king = False
        elif piece == 2:
            color = Constants.AI_COLOR
            king = False
        elif piece == 3:
            color = Constants.PLAYER_COLOR
            king = True
        elif piece == 4:
            color = Constants.AI_COLOR
            king = True
        
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
                fill=Constants.KING_COLOR,
                font=("Helvetica", max(12, int(self.game_logic.square_size/4)))
            )
    
    def on_square_clicked(self, event):
        """Handle board clicks."""
        if self.game_logic.game_over or self.game_logic.current_player != "player":
            return
        
        col = (event.x - Constants.PADDING) // self.game_logic.square_size
        row = (event.y - Constants.PADDING) // self.game_logic.square_size
        
        if not (0 <= row < self.game_logic.board_size and 0 <= col < self.game_logic.board_size):
            return
        
        if self.game_logic.selected_piece is None:
            piece = self.game_logic.board[row][col]
            if piece in (1, 3):
                self.game_logic.selected_piece = (row, col)
                self.game_logic.valid_moves = self.game_logic.get_valid_moves(row, col)
                self.draw_board()
        else:
            selected_row, selected_col = self.game_logic.selected_piece
            if (row, col) in self.game_logic.valid_moves:
                self.game_logic.make_move(selected_row, selected_col, row, col, self.player_name)
                self.game_logic.selected_piece = None
                self.game_logic.valid_moves = []
                self.draw_board()
                if not self.game_logic.game_over and self.game_logic.current_player == "ai":
                    self.master.after(500, self.ai_move)
            else:
                piece = self.game_logic.board[row][col]
                if piece in (1, 3):
                    self.game_logic.selected_piece = (row, col)
                    self.game_logic.valid_moves = self.game_logic.get_valid_moves(row, col)
                    self.draw_board()
    
    def ai_move(self):
        """Execute AI move."""
        move = self.game_logic.ai_move()
        if move:
            from_row, from_col, to_row, to_col = move
            self.game_logic.make_move(from_row, from_col, to_row, to_col, "AI")
            self.draw_board()
        else:
            self.game_logic.current_player = "player"
            self.update_status()
    
    def update_status(self):
        """Update status label."""
        if self.game_logic.game_over:
            self.status_label.config(text="Game Over!")
        elif self.game_logic.current_player == "player":
            self.status_label.config(
                text=f"{self.player_name}'s turn (Black) | {self.game_logic.ai_algorithm.capitalize()}",
                foreground="#212121"
            )
        else:
            self.status_label.config(
                text=f"AI's turn (White) | {self.game_logic.ai_algorithm.capitalize()}",
                foreground="#555555"
            )