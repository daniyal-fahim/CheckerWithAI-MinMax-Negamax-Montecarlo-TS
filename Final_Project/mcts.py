import random
import numpy as np
from copy import deepcopy
from utils import evaluate_board, is_terminal

class MCTSNode:
    """Node for Monte Carlo Tree Search."""
    
    def __init__(self, board, move, parent, game):
        self.board = deepcopy(board)
        self.move = move
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.game = game
    
    def is_terminal(self):
        """Check if node is terminal."""
        return is_terminal(self.game, self.board)
    
    def expand(self):
        """Expand node by adding children for all possible moves."""
        pieces = [(r, c) for r in range(self.game.board_size) for c in range(self.game.board_size) if self.board[r][c] in (2, 4)]
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
        """Simulate a random game from this node."""
        current_board = deepcopy(self.board)
        current_player = 'ai'
        max_steps = 50
        
        for _ in range(max_steps):
            if is_terminal(self.game, current_board):
                score = evaluate_board(self.game, current_board)
                return 1 if score > 0 else -1 if score < 0 else 0
            
            piece_types = (2, 4) if current_player == 'ai' else (1, 3)
            pieces = [(r, c) for r in range(self.game.board_size) for c in range(self.game.board_size) 
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
            elif current_board[move_row][move_col] == 1 and move_row == self.game.board_size - 1:
                current_board[move_row][move_col] = 3
            current_player = 'player' if current_player == 'ai' else 'ai'
        
        return evaluate_board(self.game, current_board) / 10
    
    def backpropagate(self, reward):
        """Backpropagate simulation results."""
        self.visits += 1
        self.wins += reward
        if self.parent:
            self.parent.backpropagate(-reward)
    
    def select_child(self):
        """Select child node using UCT formula."""
        exploration = 1.414
        return max(self.children, key=lambda c: (c.wins / c.visits if c.visits > 0 else 0) + 
                   exploration * (2 * np.log(self.visits) / c.visits)**0.5 if c.visits > 0 else float('inf'))

def mcts_move(game):
    """Monte Carlo Tree Search for AI move."""
    root = MCTSNode(game.board, None, None, game)
    iterations = 800 if game.ai_difficulty >= 3 else 400
    
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
    return best_child.move if best_child and best_child.move else None