import random
import numpy as np
from copy import deepcopy
from utils import evaluate_board, is_terminal

class MCTSNode:
    """Node for Monte Carlo Tree Search."""
    
    def __init__(self, board, move, parent, game):
        # Initialize the node with a deep copy of the game board to prevent modifying the original
        self.board = deepcopy(board)
        # Store the move that led to this node (tuple of start_row, start_col, end_row, end_col); None for root
        self.move = move
        # Reference to the parent node; None for the root node
        self.parent = parent
        # List to store child nodes, each representing a possible move from this state
        self.children = []
        # Counter for the number of times this node has been visited during MCTS iterations
        self.visits = 0
        # Accumulated reward from simulations, representing wins or scaled evaluation scores
        self.wins = 0
        # Reference to the game object, providing access to board size, rules, and utility functions
        self.game = game
    
    def is_terminal(self):
        """Check if node is terminal."""
        # Check if the current board state is terminal (game over, e.g., no pieces or no valid moves)
        # Uses the is_terminal function from utils to evaluate the board
        return is_terminal(self.game, self.board)
    
    def expand(self):
        """Expand node by adding children for all possible moves."""
        # Identify all AI pieces (2 for regular, 4 for king) on the current board
        pieces = [(r, c) for r in range(self.game.board_size) for c in range(self.game.board_size) if self.board[r][c] in (2, 4)]
        # Iterate through each AI piece to find valid moves
        for row, col in pieces:
            # Get all valid moves for the piece at (row, col) using the game's utility function
            moves = self.game.get_valid_moves_for_board(self.board, row, col)
            # Iterate through each valid move (destination coordinates)
            for move_row, move_col in moves:
                # Create a deep copy of the current board to simulate the move
                new_board = deepcopy(self.board)
                # Clear the piece's original position
                new_board[row][col] = 0
                # Move the piece to the new position
                new_board[move_row][move_col] = self.board[row][col]
                # Check if the move is a capture (jump over an opponent)
                if abs(row - move_row) == 2:
                    # Calculate the position of the captured piece (midpoint between start and end)
                    captured_row = (row + move_row) // 2
                    captured_col = (col + move_col) // 2
                    # Remove the captured piece from the board
                    new_board[captured_row][captured_col] = 0
                # Promote the AI piece to a king if it reaches the opponent's end row (row 0)
                if new_board[move_row][move_col] == 2 and move_row == 0:
                    new_board[move_row][move_col] = 4
                # Create a new child node for this move and add it to the children list
                self.children.append(MCTSNode(new_board, (row, col, move_row, move_col), self, self.game))
    
    def simulate(self):
        """Simulate a random game from this node."""
        # Create a deep copy of the current board to simulate a random game without affecting the node
        current_board = deepcopy(self.board)
        # Start with the AI as the current player (since this node represents an AI move)
        current_player = 'ai'
        # Limit the simulation to a maximum number of moves to prevent infinite loops
        max_steps = 50
        
        # Run the simulation for up to max_steps
        for _ in range(max_steps):
            # Check if the current board state is terminal (game over)
            if is_terminal(self.game, current_board):
                # Evaluate the board from the AI's perspective
                score = evaluate_board(self.game, current_board)
                # Return 1 for AI win (positive score), -1 for loss (negative score), or 0 for draw
                return 1 if score > 0 else -1 if score < 0 else 0
            
            # Determine piece types based on the current player (AI: 2, 4; opponent: 1, 3)
            piece_types = (2, 4) if current_player == 'ai' else (1, 3)
            # Identify all pieces belonging to the current player on the board
            pieces = [(r, c) for r in range(self.game.board_size) for c in range(self.game.board_size) 
                      if current_board[r][c] in piece_types]
            # If no pieces are left, the current player loses (AI: -1, opponent: 1)
            if not pieces:
                return -1 if current_player == 'ai' else 1
            
            # Randomly select a piece to move
            row, col = random.choice(pieces)
            # Get all valid moves for the selected piece
            moves = self.game.get_valid_moves_for_board(current_board, row, col)
            # If no moves are available, the current player loses
            if not moves:
                return -1 if current_player == 'ai' else 1
            
            # Randomly select a move from the valid moves
            move_row, move_col = random.choice(moves)
            # Clear the piece's original position
            current_board[row][col] = 0
            # Move the piece to the new position
            current_board[move_row][move_col] = current_board[row][col]
            # Handle capture if the move is a jump
            if abs(row - move_row) == 2:
                # Calculate the captured piece's position
                captured_row = (row + move_row) // 2
                captured_col = (col + move_col) // 2
                # Remove the captured piece
                current_board[captured_row][captured_col] = 0
            # Promote AI piece to king if it reaches the opponent's end row
            if current_board[move_row][move_col] == 2 and move_row == 0:
                current_board[move_row][move_col] = 4
            # Promote opponent piece to king if it reaches the AI's end row
            elif current_board[move_row][move_col] == 1 and move_row == self.game.board_size - 1:
                current_board[move_row][move_col] = 3
            # Switch the current player (AI to player, or player to AI)
            current_player = 'player' if current_player == 'ai' else 'ai'
        
        # If the simulation reaches max_steps, evaluate the board and scale the score
        # The score is divided by 10 to normalize it for backpropagation
        return evaluate_board(self.game, current_board) / 10
    
    def backpropagate(self, reward):
        """Backpropagate simulation results."""
        # Increment the visit counter for this node
        self.visits += 1
        # Add the simulation reward to the node's accumulated wins
        self.wins += reward
        # If this node has a parent, propagate the negated reward upwards
        # Negation accounts for alternating players (AI vs. opponent)
        if self.parent:
            self.parent.backpropagate(-reward)
    
    def select_child(self):
        """Select child node using UCT formula."""
        # Define the exploration constant for the UCT (Upper Confidence Bound for Trees) formula
        exploration = 1.414
        # Select the child with the highest UCT value, balancing exploitation and exploration
        # UCT = (wins/visits) + exploration * sqrt(2 * ln(parent_visits) / visits)
        # If visits is 0, return infinity to prioritize unvisited nodes
        return max(self.children, key=lambda c: (c.wins / c.visits if c.visits > 0 else 0) + 
                   exploration * (2 * np.log(self.visits) / c.visits)**0.5 if c.visits > 0 else float('inf'))

def mcts_move(game):
    """Monte Carlo Tree Search for AI move."""
    # Create the root node for the current game board, with no move or parent
    root = MCTSNode(game.board, None, None, game)
    # Set the number of MCTS iterations based on AI difficulty (800 for hard, 400 for easy/medium)
    iterations = 800 if game.ai_difficulty >= 3 else 400
    
    # Perform the specified number of MCTS iterations
    for _ in range(iterations):
        # Start at the root node
        node = root
        # Traverse the tree by selecting the best child (via UCT) until a leaf or terminal node is reached
        while node.children and not node.is_terminal():
            node = node.select_child()
        # If the node is not terminal, expand it by adding child nodes for all possible moves
        if not node.is_terminal():
            node.expand()
            # If children were added, randomly select one for simulation
            if node.children:
                node = random.choice(node.children)
        # Simulate a random game from the selected node to estimate its value
        reward = node.simulate()
        # Backpropagate the simulation reward up the tree to update visits and wins
        node.backpropagate(reward)
    
    # Select the child node with the most visits as the best move
    best_child = max(root.children, key=lambda c: c.visits) if root.children else None
    # Return the move associated with the best child (start_row, start_col, end_row, end_col)
    # Return None if no valid move is found (e.g., no children)
    return best_child.move if best_child and best_child.move else None