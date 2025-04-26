import tkinter as tk
from gui import CheckersGUI

def main():
    """Initialize and run the Checkers game."""
    root = tk.Tk()
    game = CheckersGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()