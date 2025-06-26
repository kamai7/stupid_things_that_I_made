from math import *

class Sudoku:
    def __init__(self, board):
        self.board = board
        self.size = len(board[0])
        self.possibilities = [i + 1 for i in range(len(board[0]))]
        self.counter = 0

        self.solution = []
        for square in self.board:
            self.solution.append([])
            for cell in square:
                self.solution[-1].append(cell)
        
    
    def solve(self):
        self.counter = 0
        res = self.backtrack(0,0)
        print(self.counter)
        return res

    def backtrack(self, line, cell):
        for i in range(line,self.size):
            for j in range(cell, self.size):
                if self.solution[i][j] == 0:
                    for num in self.possibilities:
                        if self.check(i, j, num):
                            self.counter += 1
                            self.solution[i][j] = num
                                
                            if self.backtrack(line, cell):
                                return True
                            else:
                                self.solution[i][j] = 0
                    return False
        return True
    
    def check(self, row, col, num):
        for i in range(self.size):
            if self.solution[row][i] == num:
                return False
            if self.solution[i][col] == num:
                return False
        
        block_size = int(sqrt(self.size))
        block_row = (row // block_size) * block_size
        block_col = (col // block_size) * block_size
        for i in range(block_size):
            for j in range(block_size):
                if self.solution[block_row + i][block_col + j] == num:
                    return False
        return True
    
    def display_board(self):
        for x,line in enumerate(self.solution):
            if x%int(sqrt(len(self.solution))) == 0:
                print("\n\n", end="")
            else:
                print("\n", end="")
            for y,cell in enumerate(line):
                if y%int(sqrt(len(self.solution))) == int(sqrt(len(self.solution))) - 1:
                    print(cell, end=" | ")
                else:
                    print(cell, end=" ")
        print("\n")


# Exemple de tests unitaires pour la classe Sudoku

hard_board = [
    [8, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 6, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 9, 0, 2, 0, 0],
    [0, 5, 0, 0, 0, 7, 0, 0, 0],
    [0, 0, 0, 0, 4, 5, 7, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 3, 0],
    [0, 0, 1, 0, 0, 0, 0, 6, 8],
    [0, 0, 8, 5, 0, 0, 0, 1, 0],
    [0, 9, 0, 0, 0, 0, 4, 0, 0]
]

empty_board = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

game1 = Sudoku(empty_board)

game2 = Sudoku(hard_board)
res = game1.solve()


print(res)
game1.display_board()

res2 = game2.solve()
print(res2)
game2.display_board()