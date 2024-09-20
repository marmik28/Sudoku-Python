import tkinter as tk
from tkinter import messagebox

# Predefined Sudoku puzzle (0 means the cell is empty)
PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.root.geometry("400x450")
        self.board = PUZZLE
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.create_board()

        solve_button = tk.Button(self.root, text="Solve", command=self.solve_puzzle)
        solve_button.grid(row=9, column=0, columnspan=5, sticky="nsew")

        reset_button = tk.Button(self.root, text="Reset", command=self.reset_board)
        reset_button.grid(row=9, column=5, columnspan=5, sticky="nsew")

    def create_board(self):
        """Create the grid of entry fields for Sudoku."""
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != 0:
                    cell = tk.Label(self.root, text=self.board[row][col], borderwidth=1, relief="solid", width=5, height=2)
                else:
                    cell = tk.Entry(self.root, borderwidth=1, relief="solid", width=5, justify="center")
                cell.grid(row=row, column=col)
                self.cells[row][col] = cell

    def reset_board(self):
        """Reset the board to its original state."""
        for row in range(9):
            for col in range(9):
                if isinstance(self.cells[row][col], tk.Entry):
                    self.cells[row][col].delete(0, tk.END)
                elif isinstance(self.cells[row][col], tk.Label):
                    self.cells[row][col].config(text=self.board[row][col])

    def solve_puzzle(self):
        """Solve the Sudoku puzzle and display the solution."""
        solved_board = [row[:] for row in self.board]  # Copy of the original puzzle
        if self.solve_sudoku(solved_board):
            for row in range(9):
                for col in range(9):
                    if isinstance(self.cells[row][col], tk.Entry):
                        self.cells[row][col].delete(0, tk.END)
                        self.cells[row][col].insert(0, solved_board[row][col])
        else:
            messagebox.showerror("Error", "Puzzle cannot be solved.")

    def solve_sudoku(self, board):
        """Backtracking algorithm to solve the Sudoku puzzle."""
        empty = self.find_empty_location(board)
        if not empty:
            return True  # Solved
        row, col = empty

        for num in range(1, 10):
            if self.is_safe(board, row, col, num):
                board[row][col] = num
                if self.solve_sudoku(board):
                    return True
                board[row][col] = 0  # Reset cell

        return False

    def find_empty_location(self, board):
        """Find an empty cell in the Sudoku puzzle."""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_safe(self, board, row, col, num):
        """Check if it's safe to place a number in the cell."""
        # Check row
        if num in board[row]:
            return False
        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False
        # Check 3x3 grid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[start_row + i][start_col + j] == num:
                    return False
        return True


if __name__ == "__main__":
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()
