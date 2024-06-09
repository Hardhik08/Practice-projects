import numpy as np
import tkinter as tk
from tkinter import messagebox, scrolledtext

class SudokuSolver:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku Solver")
        
        self.cells = {}
        self.board = np.zeros((9, 9), dtype=int)
        self.steps = []

        self.create_grid()
        self.create_buttons()
        self.create_step_output()

    def create_grid(self):
        for row in range(9):
            for col in range(9):
                cell = tk.Entry(self.master, width=3, font=('Arial', 18), justify='center', bd=1, relief='solid')
                
                # Configure the padding for the 3x3 grid lines
                padx = (2, 10) if col % 3 == 2 and col != 8 else (2, 2)
                pady = (2, 10) if row % 3 == 2 and row != 8 else (2, 2)
                
                cell.grid(row=row, column=col, padx=padx, pady=pady, ipady=5)
                self.cells[(row, col)] = cell

    def create_buttons(self):
        solve_button = tk.Button(self.master, text="Solve", command=self.solve_puzzle, font=('Arial', 14))
        solve_button.grid(row=9, column=0, columnspan=3, pady=20)
        
        clear_button = tk.Button(self.master, text="Clear", command=self.clear_grid, font=('Arial', 14))
        clear_button.grid(row=9, column=3, columnspan=3, pady=20)
        
        exit_button = tk.Button(self.master, text="Exit", command=self.master.quit, font=('Arial', 14))
        exit_button.grid(row=9, column=6, columnspan=3, pady=20)

    def create_step_output(self):
        self.step_output = scrolledtext.ScrolledText(self.master, width=50, height=15, font=('Arial', 12))
        self.step_output.grid(row=10, column=0, columnspan=9, pady=20)

    def clear_grid(self):
        for row in range(9):
            for col in range(9):
                self.cells[(row, col)].delete(0, tk.END)
        self.steps = []
        self.step_output.delete('1.0', tk.END)

    def get_board(self):
        for row in range(9):
            for col in range(9):
                value = self.cells[(row, col)].get()
                if value.isdigit():
                    self.board[row, col] = int(value)
                else:
                    self.board[row, col] = 0
        return self.board

    def display_board(self, board):
        for row in range(9):
            for col in range(9):
                if board[row, col] != 0:
                    self.cells[(row, col)].delete(0, tk.END)
                    self.cells[(row, col)].insert(0, str(board[row, col]))

    def log_step(self, row, col, num):
        self.steps.append(f"Placed {num} in cell ({row+1}, {col+1})")
        self.step_output.insert(tk.END, f"Placed {num} in cell ({row+1}, {col+1})\n")
        self.step_output.see(tk.END)

    def is_valid(self, board, row, col, num):
        for i in range(9):
            if board[row, i] == num or board[i, col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i, j] == num:
                    return False
        return True

    def solve(self, board):
        for row in range(9):
            for col in range(9):
                if board[row, col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row, col] = num
                            self.log_step(row, col, num)
                            if self.solve(board):
                                return True
                            board[row, col] = 0
                    return False
        return True

    def solve_puzzle(self):
        self.step_output.delete('1.0', tk.END)
        self.steps = []
        self.get_board()
        if self.solve(self.board):
            self.display_board(self.board)
            messagebox.showinfo("Success", "Sudoku solved successfully!")
        else:
            messagebox.showerror("Failure", "No solution exists for the given Sudoku puzzle.")

if __name__ == "__main__":
    root = tk.Tk()
    solver = SudokuSolver(root)
    root.mainloop()
