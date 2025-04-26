# CheckerWithAI
# CheckerWithAI-MinMax-Negamax-Montecarlo-TS

Advanced Checkers Game with AI
Overview
This project is an Advanced Checkers Game developed as a desktop application using Python. It features a user-friendly graphical interface built with Tkinter and implements three distinct AI algorithms—Minimax, Negamax, and Monte Carlo Tree Search (MCTS)—to provide challenging opponents for the player. The game supports customizable settings, such as player name, AI difficulty, and algorithm selection, making it both an entertaining game and an educational tool for studying AI techniques in game development.
This project was developed as part of an Artificial Intelligence course at the National University of Computer & Emerging Sciences, Karachi Campus.
Features

Interactive Checkers Gameplay: Play Checkers (Draughts) with standard rules, including captures, king promotions, and mandatory jumps.
Multiple AI Algorithms:
Minimax with alpha-beta pruning for deterministic move evaluation.
Negamax with alpha-beta pruning for efficient AI decision-making.
Monte Carlo Tree Search (MCTS) for probabilistic, simulation-based moves.


Customizable Settings:
Enter a player name.
Choose AI difficulty: Easy (depth 2 or 400 MCTS iterations), Medium (depth 3 or 800 iterations), Hard (depth 5 or 800 iterations).
Select AI algorithm (Minimax, Negamax, MCTS).


Modern GUI:
Responsive Tkinter-based interface with a resizable board.
Visual feedback for selected pieces and valid moves.
Modern color scheme with gradient-style pieces and king indicators.


Move History: Track and review all moves in a separate window.
Game Over Detection: Automatically detects win/loss conditions (no pieces or no valid moves) with pop-up notifications.
Performance Insights: Displays AI move computation times in the console for educational purposes.
Cross-Platform: Runs on Windows, Linux, and macOS.

Project Structure
The project is organized in the final_project directory with the following files:
final_project/
├── main.py              # Entry point to run the game
├── gui.py               # Handles Tkinter GUI (start screen, board, settings)
├── game_logic.py        # Manages game rules, board state, and move validation
├── minimax.py           # Implements Minimax algorithm with alpha-beta pruning
├── negamax.py           # Implements Negamax algorithm with alpha-beta pruning
├── mcts.py              # Implements Monte Carlo Tree Search algorithm
├── utils.py             # Contains constants and utility functions
└── run_game.sh          # Bash script to install dependencies and run the game

Requirements

Python 3+: Required to run the game.
Tkinter: Included with standard Python installations (may need python3-tk on some Linux systems).
NumPy: Used for efficient board representation (installed via the Bash script).
Operating System: Windows, Linux, or macOS.

Setup Instructions
1. Clone or Download the Project
Ensure you have the project files in a directory. The code should be placed in a final_project folder, and the run_game.sh script should be in the parent directory or the same directory.
2. Verify Directory Structure
Confirm that the final_project directory contains:

main.py
gui.py
game_logic.py
minimax.py
negamax.py
mcts.py
utils.py

The run_game.sh script should be accessible (e.g., in the parent directory).
3. Make the Bash Script Executable (Linux/macOS)
chmod +x run_game.sh

4. Run the Game
Navigate to the final_project directory.
Check for Python 3 and pip.
Install NumPy if not already installed.
Run main.py to start the game.

Manual Execution (Any Platform)
If you prefer not to use the Bash script:
cd final_project
pip install numpy
python main.py

5. Troubleshooting

Tkinter Not Found: On Linux, install Tkinter with:sudo apt-get install python3-tk  # Ubuntu/Debian
sudo dnf install python3-tkinter  # Fedora


NumPy Installation Fails: Ensure you have an internet connection and pip is up-to-date:pip install --upgrade pip


Directory Error: If run_game.sh reports that final_project is missing, verify the directory exists in the same location as the script.

Usage

Start Screen:

Enter your name.
Select AI difficulty (Easy, Medium, Hard).
Choose an AI algorithm (Minimax, Negamax, MCTS).
Click "Start Game" to begin.


Gameplay:

Play as Black pieces against the AI (White pieces).
Click a piece to select it (highlighted in green).
Valid moves are shown with light green circles.
Click a valid move to execute it.
The AI responds automatically after your move.


Settings:

Click the "⚙ Settings" button to adjust difficulty or algorithm during the game.
Changes take effect immediately.


Move History:

Click the "📜 History" button to view all moves in a separate window.


Game Over:

The game ends when a player has no pieces or no valid moves.
A pop-up displays the winner.



Development Details

Programming Language: Python 3
Libraries:
Tkinter: For the graphical interface.
NumPy: For efficient board manipulation.
Standard Libraries: copy, random, time


AI Algorithms:
Minimax and Negamax use alpha-beta pruning for efficiency.
MCTS uses 400 (Easy) or 800 (Medium/Hard) iterations for simulation-based decisions.


Design:
Modular code structure with separate files for GUI, game logic, and AI algorithms.
Responsive GUI with a modern color scheme and visual feedback.
Optimized for performance on modest hardware.



Contributing
Contributions are welcome! To contribute:

Fork the repository (if hosted on a platform like GitHub).
Create a new branch for your feature or bug fix.
Submit a pull request with a clear description of changes.

Please ensure code follows PEP 8 guidelines and includes appropriate comments/docstrings.
License
This project is licensed under the MIT License. See the LICENSE file for details (if included).
Contact
For questions or feedback, please contact the project team:

Daniyal Fahim (22k-4282)
Daiyan Ur Rehman (22k-4167)
Dawood Adnan (22k-4663)

Developed for the Artificial Intelligence course at NUCES, Karachi Campus, April 2025.
