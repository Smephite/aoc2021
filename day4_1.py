from typing import Dict, List
import aoc

from typing import Dict, List
import aoc

class Bingo:
    grid : Dict[int, int]
    completed : List[int]
    grid_size : int


    def __init__(self, grid: List[List[int]]):
        self.grid = {}
        self.completed = []
        self.grid_size = len(grid)
        for i_row in range(0, len(grid)):
            row = grid[i_row]
            
            assert(len(row) == len(grid)) # input must be square

            for i_col in range(0, len(row)):
                self.grid[len(row)*i_row+i_col] = int(row[i_col])


    def check_complete(self, new_pos):
        # We need at least 5 completed fields for a bingo
        if len(self.completed) < 5:
            return False

        # extract position from array index
        row = int(new_pos / self.grid_size)
        col = new_pos - row*self.grid_size
        
        # Check for completion by checking row and column of newest field
        col_complete = True
        for i in range(row*self.grid_size, (row+1)*self.grid_size):
            if i not in self.completed:
                col_complete = False
                break

        row_complete = True
        for i in range(0, self.grid_size):
            pos = i*self.grid_size+col
            if pos not in self.completed:
                row_complete = False
                break
        
        return row_complete or col_complete


    def get_uncompleted(self):
        return list(map(lambda pos: self.grid[pos], filter(lambda pos: pos not in self.completed, self.grid.keys())))
            

#
# Parse Input
#

input = aoc.aoc()

numbers = list(map(lambda x: int(x), input.pop(0).split(","))) # this is to not parse the numbers as bingo area
input.append('') # this is to flush the last bingo area
boards : List[Bingo] = [] 
current_board = []
for line in input:
    if line == '':
        if len(current_board) != 0:
            boards.append(Bingo(current_board))
            current_board = []
    else:
        current_board.append(list(map(lambda n: int(n), filter(lambda n: n != '', line.split(' ')))))


#
# Simulate the games
#

best_board = None
last_num = None
for number in numbers:
    last_num = number
    containing_boards = list(filter(lambda b: number in b.grid.values(), boards))

    for board in containing_boards:
        pos = list(board.grid.values()).index(number)
        board.completed.append(pos)

        if board.check_complete(pos):
            best_board = board
            break
    
    if best_board is not None:
        break


print(f"Found best board to be {str(best_board.grid)}!")
print(f"Board will win with number {last_num}")
print("The score gained is", sum(best_board.get_uncompleted()) * last_num)